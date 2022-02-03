from curses.ascii import HT
from aiocqhttp import HttpFailed
from httpx import AsyncClient, HTTPError
from .log import logger

class ServiceException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    @property
    def message(self) -> str:
        return self.args[0]

async def fetch_text(uri: str) -> str:
    async with AsyncClient(headers={ 'User-Agent': 'box-s-ville.ioabot' }) as client:
        try:
            res = await client.get(uri)
            res.raise_for_status()
        except HTTPError as e:
            logger.exception(e)
            raise ServiceException('API 服务目前无法使用')
        return res.text