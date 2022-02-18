"""
The model of messages that in a QQ group
"""
# pylint: disable=no-member
# gino has no ... member
from services.db_context import db


class GroupMsg(db.Model):
    """
    The model of messages that in a QQ group
    """

    __tablename__ = "group_msgs"

    id = db.Column(db.Integer(), primary_key=True)
    belonging_user = db.Column(db.BigInteger(), db.ForeignKey("group_users.id"))
    belonging_group = db.Column(db.BigInteger(), db.ForeignKey("groups.id"))

    sent_time = db.Column(db.DateTime(timezone=True), nullable=False)
    raw_msg = db.Column(db.String())
    text_msg = db.Column(db.String())
