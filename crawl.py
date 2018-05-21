from sample import AsyncSample
from threading import Thread
import asyncio


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == '__main__':
    # 链接抓取
    max_page = 1000  # 读取的页数
    loop = asyncio.new_event_loop()
    crawler = AsyncSample(max_page, max_tasks=50,
                          _loop=loop)  # 协程数量 采集url
    t = Thread(target=start_loop, args=(loop,), name="lianjia")
    t.start()
    asyncio.run_coroutine_threadsafe(crawler.run(), loop)

    # # # 本地线程执行
    # max_page = 1000
    # loop = asyncio.get_event_loop()
    # crawler = AsyncSample(max_page, max_tasks=66)  # 协程数量 采集url
    # loop.run_until_complete(crawler.run())
    # loop.close()
