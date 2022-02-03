import os
from gino import Gino
from config import DATABASE_URI
from .log import logger

db = Gino()

async def init():
    await db.set_bind(DATABASE_URI)
    await db.gino.create_all()
    logger.info(f'Database loaded successfully!')