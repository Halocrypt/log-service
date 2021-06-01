from .shared import db

from .log import Logs


# pylint: disable=E1101
def commit():
    db.session.commit()


def add_to_db(l: Logs):
    db.session.add(l)
