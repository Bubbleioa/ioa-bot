from datetime import datetime
import nonebot

from services.log import logger
from models.group_msg import GroupMsg
from models.group_user import GroupUser

bot = nonebot.get_bot()


@bot.on_message("group")
async def handle_group_msg(session):
    """
    将群消息存入数据库
    """
    user = await GroupUser.ensure(session["user_id"], session["group_id"])
    raw_message = session["raw_message"]
    text_message = ""

    flag = 0
    for c in raw_message:
        if c == "[":
            flag += 1
        elif c == "]":
            flag -= 1
        if flag == 0:
            text_message += c

    await GroupMsg.create(
        belonging_user=user.id,
        belonging_group=user.belonging_group,
        sent_time=datetime.now(),
        raw_msg=raw_message,
        text_msg=text_message,
    )

    logger.info(f"{user.id} 发送了消息，纯文本格式： {text_message}")
