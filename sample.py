from datetime import datetime
from asyncio import Queue
import aiohttp
import asyncio
import csv


class AsyncSample(object):

    def __init__(self, max_page, max_tries=2, max_tasks=10, _loop=None):
        self.loop = _loop or asyncio.get_event_loop()
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.urls_queue = Queue(loop=self.loop)
        self.file = 'lianjia.csv'
        self.base_url = 'http://sh.lianjia.com/'
        self.seen_urls = set()
        data_dict ={}
        self.sleep_interval = 0.1
        # self.session = aiohttp.ClientSession(loop=self.loop)
        self.create_csv(('index', 'name'))
        self.get_url(max_page)
        self.started_at = datetime.now()
        self.end_at = None

    def create_csv(self, fields):
        with open(self.file, 'w', newline='') as f:
            if isinstance(fields, tuple):
                f_csv = csv.writer(f)
                f_csv.writerow(fields)
            else:
                print("csv列名称数据类型错误")

    def get_url(self, max_page):
        for x in range(max_page):
            self.urls_queue.put_nowait(x)

    def close(self):
        self.session.close()

    def write_to_csv(self, value):
        with open(self.file, 'a+', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(value)

    async def handle(self, url):
        tries = 0
        while tries < self.max_tries:
            try:
                # response = await self.session.get(url, allow_redirects=False)
                break
            except aiohttp.ClientError:
                pass
            tries += 1
        try:
            value = [str(url), str(url+1)]
            self.write_to_csv(value)
        finally:
            pass
            # await response.release()

    async def work(self):
        try:
            while True:
                url = await self.urls_queue.get()
                await self.handle(url)
                self.urls_queue.task_done()
                await asyncio.sleep(self.sleep_interval)
        except asyncio.CancelledError:
            pass

    async def run(self):
        workers = [asyncio.Task(self.work(), loop=self.loop) for _ in range(self.max_tasks)]
        self.started_at = datetime.now()
        await self.urls_queue.join()
        self.end_at = datetime.now()
        for w in workers:
            w.cancel()
        # self.close()
        print('Finished {0} urls in {1} secs'.format(len(self.seen_urls),
                                                     (self.end_at - self.started_at).total_seconds()))
        self.loop.close()
        print('Finished {0} urls in {1} secs'.format(len(self.seen_urls),
                                                     (self.end_at - self.started_at).total_seconds()))
