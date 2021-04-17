from flask import Flask, request
from server.constants import DATABASE_URL

from server.models import db

app = Flask(__name__)

database_url: str = DATABASE_URL

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.errorhandler(404)
def catch_all(e):
    return "not found"


@app.errorhandler(405)
def method_not_allowed(e):
    return "Method not allowed"


@app.after_request
def cors(resp):

    resp.headers["access-control-allow-origin"] = request.headers.get("origin") or "*"
    resp.headers["access-control-allow-headers"] = request.headers.get(
        "access-control-request-headers", "*"
    )
    resp.headers["access-control-allow-credentials"] = "true"
    resp.headers["x-dynamic"] = "true"
    resp.headers["access-control-max-age"] = "86400"
    return resp
