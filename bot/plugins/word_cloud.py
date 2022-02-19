from datetime import datetime, timedelta
from io import BytesIO
from base64 import b64encode
import pytz
import nonebot
import jieba
import wordcloud
from aiocqhttp.message import MessageSegment
from models.group import Group
from models.group_msg import GroupMsg
from config import RESOURCES_DIR


@nonebot.scheduler.scheduled_job("cron", day="*", hour=1)
async def gen_word_cloud(delta=1):
    """
    生成每日词云
    """
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone("Asia/Shanghai"))
    all_groups = await Group.query.gino.all()
    for group in all_groups:
        words = []
        wc = wordcloud.WordCloud(
            width=1000,
            height=700,
            background_color="white",
            font_path=f"{RESOURCES_DIR}/LXGWWenKai-Regular.ttf",
            # font_path="/home/ioa/code/ioa-bot/bot/resources/LXGWWenKai-Regular.ttf",
        )
        msgs = await GroupMsg.query.where(
            GroupMsg.belonging_group == group.id
        ).gino.all()
        for msg in msgs:
            if now.date() - msg.sent_time.date() == timedelta(days=delta):
                words += jieba.lcut(msg.text_msg)
        string = " ".join(words)
        wc.generate(string)

        image = wc.to_image()
        buff = BytesIO()
        image.save(buff, "jpeg")
        im_b64 = b64encode(buff.getvalue()).decode()
        await bot.send_group_msg(
            group_id=group.group_id, message=MessageSegment.image(f"base64://{im_b64}")
        )
