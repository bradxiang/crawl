from sample import AsyncSample
from threading import Thread
import asyncio
import time


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == '__main__':

    # 本地线程执行
    # loop = asyncio.get_event_loop()
    # crawler = AsyncSample(max_tasks=20, _loop=loop)  # 协程数量 采集url
    # loop.run_until_complete(crawler.run())

    # 创建新线程异步操作，永久运行线程
    new_loop = asyncio.new_event_loop()
    t = Thread(target=start_loop, args=(new_loop,))
    t.setDaemon(True)  # 设置子线程为守护线程
    t.start()
    try:
        while True:
            crawler = AsyncSample(max_tasks=20,
                                  _loop=new_loop)  # 协程数量 采集url
            future = asyncio.run_coroutine_threadsafe(crawler.run(), new_loop)
            while not future.done():
                time.sleep(0.1)
    except KeyboardInterrupt as e:
        new_loop.stop()

