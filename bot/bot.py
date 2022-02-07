from os import path
import nonebot
import config
from services import db_context

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.on_startup(db_context.init)
    nonebot.run()