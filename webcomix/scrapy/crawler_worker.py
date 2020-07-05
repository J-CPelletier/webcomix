import signal
from multiprocessing import Process, Queue

from pydispatch import dispatcher
from scrapy import signals
from scrapy.crawler import CrawlerProcess


class CrawlerWorker(Process):
    def __init__(self, settings, return_items, *crawl_args, **crawl_kwargs):
        super().__init__(daemon=True)
        self.result_queue = Queue()
        self.crawl_args = crawl_args
        self.crawl_kwargs = crawl_kwargs

        self.process = CrawlerProcess(settings)
        self.kill_process = False
        dispatcher.connect(self._spider_error, signals.spider_error)
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)

    def _spider_error(self, failure):
        self.result_queue.put(failure.value)

    def _exit_gracefully(self, signum, frame):
        self.kill_process = True
        self.process.stop()

    def run(self):
        self.process.crawl(
            *self.crawl_args, **self.crawl_kwargs, result_queue=self.result_queue
        )
        self.process.start()

    def start(self):
        super().start()
        super().join()

        result = []
        while not self.result_queue.empty():
            result.append(self.result_queue.get())

        if self.kill_process:
            raise KeyboardInterrupt
        if len(result) == 1 and isinstance(result[0], Exception):
            raise result[0]
        elif not result:
            return None
        else:
            return result
