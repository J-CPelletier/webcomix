import signal
from multiprocessing import Process, Queue

from pydispatch import dispatcher
from scrapy import signals
from scrapy.crawler import CrawlerProcess


class CrawlerWorker(Process):
    def __init__(self, settings, return_items, *crawl_args, **crawl_kwargs):
        super(CrawlerWorker, self).__init__()
        self.result_queue = Queue()
        self.crawl_args = crawl_args
        self.crawl_kwargs = crawl_kwargs

        self.process = CrawlerProcess(settings)
        self.kill_process = False
        self.items = []
        dispatcher.connect(self._spider_error, signals.spider_error)
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)
        if return_items:
            dispatcher.connect(self._add_item, signals.item_scraped)

    def _add_item(self, item):
        self.items.append(item)

    def _spider_error(self, failure):
        self.result_queue.put(failure.value)

    def _exit_gracefully(self, signum, frame):
        self.kill_process = True
        self.process.stop()

    def run(self):
        self.process.crawl(*self.crawl_args, **self.crawl_kwargs)
        self.process.start()
        if self.result_queue.empty():
            self.result_queue.put(self.items)

    def start(self):
        super(CrawlerWorker, self).start()

        result = self.result_queue.get()

        if self.kill_process:
            raise KeyboardInterrupt
        if isinstance(result, Exception):
            raise result
        elif not result:
            return None
        else:
            return result
