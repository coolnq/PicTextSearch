import asyncio

from demo.code.config import logger
from PicTextSearch import Network, Yandex
from PicTextSearch.model import YandexResponse
from PicTextSearch.sync import Yandex as YandexSync


@logger.catch()
async def demo_async() -> None:
    async with Network() as client:
        engine = Yandex(client=client)
        resp = await engine.search("кот в сапогах")
        show_result(resp)


@logger.catch()
def demo_sync() -> None:
    yandex = YandexSync()
    resp = yandex.search("кот в сапогах")
    show_result(resp)  # pyright: ignore[reportArgumentType]


def show_result(resp: YandexResponse) -> None:
    # logger.info(resp.origin)  # Original data
    logger.info(resp.url)  # Link to search results
    # logger.info(resp.raw[0].origin)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].source)
    logger.info(resp.raw[0].content)
    logger.info(resp.raw[0].size)
    logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(demo_async())
    # demo_sync()
