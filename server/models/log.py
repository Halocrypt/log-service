from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList

from .shared import db


class Logs(db.Model):
    # pylint: disable=E1101
    user: str = db.Column(db.String(30), primary_key=True)
    actions: list = db.Column(MutableList.as_mutable(JSONB))
    # pylint: enable=E1101

    def __init__(self, user: str = None, actions: list = []):

        self.user = user
        self.actions = actions
