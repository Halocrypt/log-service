from flask import send_from_directory, request
import json

from flask.json import jsonify
from set_env import setup_env

setup_env()
from server.app_init import app
from server.constants import ACCESS_KEY, IS_PROD
from server.models import Logs, add_to_db, commit


def is_authenticated():
    # if not IS_PROD:
    #     return True
    return request.headers.get("x-access-key") == ACCESS_KEY


def serve_static_file(file: str):
    ONE_YEAR_IN_SECONDS = 60 * 60 * 24 * 365
    # we disallow all bots here because we don't want useless crawling over the API
    return send_from_directory("static", file, cache_timeout=ONE_YEAR_IN_SECONDS)


@app.route("/robots.txt")
def robots():
    return serve_static_file("robots.txt")


@app.route("/")
def all_logs():
    if not is_authenticated():
        return "Hi, No."
    limit = int(request.args.get("limit", 0))

    logs = []
    for x in Logs.query.all():
        for i in x.actions:
            logs.append([x.user, *i])
    # sort by timestamp
    logs.sort(key=lambda x: x[4], reverse=True)
    return jsonify({"data": logs[:limit] if limit else logs})


def get_previous_logs(user):
    l: Logs = Logs.query.filter_by(user=user).first()
    if l:
        a = l.actions
        l.actions = a
        return a
    l = Logs(user)
    add_to_db(l)
    return l.actions


@app.route("/add", methods=["post"])
def add_logs():
    if not is_authenticated():
        return "No."
    # Array<[User, Question, Answer, Timestamp, isCorrect]>
    data = request.get_data(as_text=True)
    unparsed = filter(bool, data.splitlines())
    js = [json.loads(x) for x in unparsed]
    prev = {}
    for i in js:
        user, *rest = i
        previous_logs = prev.get(user)
        if not previous_logs:
            previous_logs = get_previous_logs(user)
            prev[user] = previous_logs
        previous_logs.append(rest)
    commit()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
