from nonebot.command import CommandSession
from nonebot.plugin import on_command
from .word_cloud import gen_word_cloud

__plugin_name__ = "ping"
__plugin_usage__ = "用法：对我说 ping 我回复 pong！"


@on_command("ping", permission=lambda sender: sender.is_superuser)
async def _(session: CommandSession):
    await session.send("pong!")
    await gen_word_cloud(delta=0)
