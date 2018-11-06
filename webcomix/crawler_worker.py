from multiprocessing import Process, Queue

from scrapy import signals
from scrapy.crawler import CrawlerProcess
from pydispatch import dispatcher


class CrawlerWorker(Process):
    def __init__(self, settings, return_items, *crawl_args, **crawl_kwargs):
        super(CrawlerWorker, self).__init__()
        self.result_queue = Queue()
        self.crawl_args = crawl_args
        self.crawl_kwargs = crawl_kwargs

        self.process = CrawlerProcess(settings)
        self.items = []
        if return_items:
            dispatcher.connect(self._add_item, signals.item_scraped)

    def _add_item(self, item):
        self.items.append(item)

    def run(self):
        try:
            self.process.crawl(*self.crawl_args, **self.crawl_kwargs)
            self.process.start()
            self.process.stop()
            self.result_queue.put(self.items)
        except Exception as exception:
            self.result_queue.put(exception)

    def start(self):
        super(CrawlerWorker, self).start()

        result = self.result_queue.get()

        if isinstance(result, Exception):
            raise result
        elif not result:
            return None
        else:
            return result
