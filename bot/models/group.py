"""
The model of group that contains group settings
"""
from services.db_context import db

# pylint: disable=no-member
# gino has no ... member


class Group(db.Model):
    """
    The model of group that contains group settings
    """

    __tablename__ = "groups"
    id = db.Column(db.Integer(), primary_key=True)
    group_id = db.Column(db.BigInteger(), nullable=False, unique=True)
