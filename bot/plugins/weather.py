'''
weather plugin
'''
from nonebot import IntentCommand, NLPSession, on_natural_language
from nonebot.command import CommandSession
from nonebot.plugin import on_command
from config import SELFNAME
from services.common import ServiceException
from services.weather import get_current_weather_short, get_current_weather_desc
from jieba import posseg

__plugin_name__ = '天气'
__plugin_usage__ = '用法： /天气 + 地名 + [详细]'

@on_natural_language(keywords={'天气'})
async def _(session: NLPSession):
    words = posseg.lcut(session.msg_text.strip())
    args = {}
    for word in words:
        if word.flag == 'ns':
            args['city'] = word.word
        elif word.word in ('详细', '报告', '详情'):
            args['is_detailed'] = True
    return IntentCommand(90, 'weather', args=args)

@on_command('weather',aliases=('天气', '气温'))
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split(' ', 1)
    if not args[0]:
        city = await session.aget(key='city',prompt=f'请问是哪做城市呢？{SELFNAME}会过来找 你 哦w', at_sender=True)
    else : city = args[0]
    is_detailed = (len(args)==2 and args[1]=='详细') or session.state.get('is_detailed')
    try:
        func = get_current_weather_desc if is_detailed else get_current_weather_short
        result = await func(city)
    except ServiceException as error:
        result = error.message

    await session.send(result)