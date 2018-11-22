from multiprocessing import Process, Queue

import click
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from pydispatch import dispatcher


class CrawlerWorker(Process):
    def __init__(self, settings, return_items, *crawl_args, **crawl_kwargs):
        super(CrawlerWorker, self).__init__()
        self.result_queue = Queue()
        self.crawl_args = crawl_args
        self.crawl_kwargs = crawl_kwargs

        self.inner_exception = None

        self.process = CrawlerProcess(settings)
        self.items = []
        dispatcher.connect(self._spider_error, signals.spider_error)
        if return_items:
            dispatcher.connect(self._add_item, signals.item_scraped)

    def _add_item(self, item):
        self.items.append(item)

    def _spider_error(self, failure):
        self.result_queue.put(failure.value)
        self.result_queue.put(failure.getTraceback())

    def run(self):
        self.process.crawl(*self.crawl_args, **self.crawl_kwargs)
        self.process.start()
        if self.result_queue.empty():
            self.result_queue.put(self.items)

    def start(self):
        super(CrawlerWorker, self).start()

        result = self.result_queue.get()

        if isinstance(result, Exception):
            inner_exception = self.result_queue.get()
            click.echo("Error inside of Crawler Worker:")
            click.echo(inner_exception)
            click.echo("-------------------------------")
            click.echo("Error outside of Crawler Worker:")
            raise Exception(result)
        elif not result:
            return None
        else:
            return result