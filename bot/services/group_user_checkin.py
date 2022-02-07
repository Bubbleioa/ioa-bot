import asyncio
import random
from datetime import datetime
from io import BytesIO
from base64 import b64encode 

from PIL import Image, ImageDraw, ImageFont

from .log import logger
from .db_context import db
from .processpool import processpool_executor  
from models.group_user import GroupUser
from config import SELFNAME, RESOURCES_DIR

async def group_user_check_use_b64img(user_qq: int, group: int, user_name: str) -> str:
    'Returns the base64 image representation of the user check result.'
    user = await GroupUser.ensure(user_qq, group)

    # expensive operation!
    return await asyncio.get_event_loop().run_in_executor(
        processpool_executor,
        _create_user_check_b64img,
        user_name, user,
    )

def _create_user_check_b64img(user_name: str, user: GroupUser) -> str:
    # 图像的参数是凭感觉来的
    # TODO: we have a lot of byte copies. we have to optimise them.
    bg_dir = f'{RESOURCES_DIR}/超天酱.jpg'
    font_dir = f'{RESOURCES_DIR}/LXGWWenKai-Regular.ttf'

    left = Image.open(bg_dir)
    left = left.crop(random.choice((
        (0,0,600,525),
        (600,525,1200,1050),
        (600,0,1200,525),
        (0,525,600,1050))
    ))
    bg = Image.new('RGB',(300,525),(255,255,255))
    image = Image.new('RGB',(900,525),(0,0,0))
    image.paste(left)
    image.paste(bg,(600,0))

    draw = ImageDraw.ImageDraw(image)
    font_title = ImageFont.truetype(font_dir, 33 if len(user_name) < 8 else 28)
    font_detail = ImageFont.truetype(font_dir, 22)

    txt_user = f'{user_name} ({user.user_qq})'
    draw.text((600, 90), txt_user, fill=(0, 0, 0), font=font_title, stroke_width=1, stroke_fill='#7042ad')

    txt_detail = (
        f'群: {user.belonging_group}\n'
        f'好感度: {user.impression:.02f}\n'
        f'签到次数: {user.checkin_count}\n'
        f'上次签到: {user.checkin_time_last.strftime("%Y-%m-%d") if user.checkin_count else "从未"}'
    )
    draw.text((600, 140), txt_detail, fill=(0, 0, 0), font=font_detail, stroke_width=1, stroke_fill='#75559e')

    buff = BytesIO()
    image.save(buff, 'jpeg')
    return b64encode(buff.getvalue()).decode()

async def group_user_check_in(user_qq: int, group: int) -> str:
    present = datetime.now()
    async with db.transaction():
        user = await GroupUser.ensure(user_qq, group, for_update = True)
        if user.checkin_time_last.date() == present.date():
            return _handle_already_checked_in(user)
        return await _handle_check_in(user)

def _handle_already_checked_in(user: GroupUser) -> str:
    return f'今天已经签到过啦，好感度：{user.impression:.2f}'

async def _handle_check_in(user: GroupUser) -> str:
    impression_added = random.random()
    new_impression = user.impression + impression_added
    message = random.choice((
        f'{SELFNAME}最喜欢你啦w',
        '谢谢，你是个好人！',
        '对了，来喝杯茶吗？'
    ))
    await user.update(
        checkin_count=user.checkin_count + 1,
        checkin_time_last=datetime.now(),
        impression=new_impression,
    ).apply()

    logger.info(f'(USER {user.user_qq}, GROUP {user.belonging_group}) CHECKED IN successfully. score: {new_impression:.2f} (+{impression_added:.2f}).')

    return f'{message} 好感度：{new_impression:.2f} (+{impression_added:.2f})'

async def group_user_check(user_qq: int, group: int) -> str:
    # heuristic: if users find they have never checked in they are probable to check in
    user = await GroupUser.ensure(user_qq, group)
    return '好感度：{:.2f}\n历史签到数：{}\n上次签到日期：{}'.format(
        user.impression,
        user.checkin_count,
        user.checkin_time_last.strftime('%Y-%m-%d') if user.checkin_time_last != datetime.min else '从未',
    )