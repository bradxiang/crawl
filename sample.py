from datetime import datetime
from asyncio import Queue
import aiohttp
import asyncio
import csv


class AsyncSample(object):

    def __init__(self, max_tasks=10, _loop=None, max_tries=2):
        self.loop = _loop or asyncio.new_event_loop()
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.urls_queue = Queue(loop=self.loop)
        self.file = ['./data/'+str(i)+'.csv' for i in range(10)]
        self.sleep_interval = 0.1
        self.create_csv(('index', 'name'))
        self.get_url(1000)
        self.started_at = datetime.now()
        self.end_at = None

    def create_csv(self, fields):
        for file_name in self.file:
            with open(file_name, 'a+', newline='') as f:
                if isinstance(fields, tuple):
                    f_csv = csv.writer(f)
                    f_csv.writerow(fields)
                else:
                    print("csv列名称数据类型错误")

    def get_url(self, max_page):
        for x in range(max_page):
            self.urls_queue.put_nowait(x)

    def write_to_csv(self, value):
        file_name = self.file[int(value[0]) % 10]
        with open(file_name, 'a+', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(value)

    async def handle(self, data):
        try:
            value = [str(x) for x in range(data, 1024)]
            self.write_to_csv(value)
        finally:
            pass

    async def work(self):
        try:
            while True:
                data = await self.urls_queue.get()
                await self.handle(data)
                self.urls_queue.task_done()
        except asyncio.CancelledError:
            pass

    async def run(self):
        workers = [asyncio.Task(self.work(), loop=self.loop) for _ in range(self.max_tasks)]
        self.started_at = datetime.now()
        await self.urls_queue.join()
        self.end_at = datetime.now()
        for w in workers:
            w.cancel()
        print('Finished work in {0} secs'.format((self.end_at - self.started_at).total_seconds()))

