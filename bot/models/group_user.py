"""
The model of users that in a QQ group
"""
# pylint: disable=no-member
# gino has no ... member
from datetime import datetime

from services.log import logger
from services.db_context import db
from .group import Group


class GroupUser(db.Model):
    """The model of users that in a QQ group"""

    __tablename__ = "group_users"

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    belonging_group = db.Column(db.BigInteger(), db.ForeignKey("groups.id"))

    checkin_count = db.Column(db.Integer(), nullable=False)
    checkin_time_last = db.Column(db.DateTime(timezone=True), nullable=False)
    impression = db.Column(db.Numeric(scale=3, asdecimal=False), nullable=False)

    _idx1 = db.Index("group_users_idx1", "user_qq", "belonging_group", unique=True)

    @classmethod
    async def ensure(
        cls, user_qq: int, belonging_group: int, for_update: bool = False
    ) -> "GroupUser":
        """
        ensure user exists
        """
        group_id = (
            await Group.select("id")
            .where(Group.group_id == belonging_group)
            .gino.scalar()
        )

        logger.info(f"group_id = {group_id}")
        if not group_id:
            new_group = await Group.create(group_id=belonging_group)
            belonging_group = new_group.id
        else:
            belonging_group = group_id

        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        if for_update:
            query = query.with_for_update()
        user = await query.gino.first()

        logger.info(f"{belonging_group}")
        return user or await cls.create(
            user_qq=user_qq,
            belonging_group=belonging_group,
            checkin_count=0,
            checkin_time_last=datetime.min,
            impression=0,
        )
