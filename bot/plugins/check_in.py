'''
check in plugin
'''
from aiocqhttp.message import MessageSegment
from nonebot import get_bot, CommandSession, on_command

from services.group_user_checkin import group_user_check_in, group_user_check_use_b64img

__plugin_name__ = '签到'
__plugin_usage__ = (
    '用法：\n'
    '对我说alpine “签到” 来签到\n'
    '“我的签到” 来获取历史签到信息'
)

checkin_permission = lambda sender: sender.is_groupchat

@on_command('签到',permission=checkin_permission)
async def _(session:CommandSession):
    await session.send(
        await group_user_check_in(session.event.user_id, session.event.group_id),
        at_sender = True
    )

@on_command('我的签到',aliases={'好感度'}, permission=checkin_permission)
async def _(session:CommandSession):
    user_id, group_id = session.event.user_id, session.event.group_id
    nickname = (await get_bot().get_stranger_info(user_id=user_id))['nickname']
    im_b64 = await group_user_check_use_b64img(user_id, group_id, nickname)
    await session.send(
        MessageSegment.image(f'base64://{im_b64}'),
        at_sender = True
    )