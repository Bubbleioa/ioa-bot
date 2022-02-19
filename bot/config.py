import logging
import os
from nonebot.default_config import *

SUPERUSERS = {1342130847}
COMMAND_START = {"/", ""}
NICKNAME = {"超天酱"}
SELFNAME = "超天酱"
HOST = "0.0.0.0"
PORT = 8702
DEBUG = True
RESOURCES_DIR = "resources"
DATABASE_URI = os.environ["DATABASE_URI"]
LOGGING_LEVEL = logging.INFO
