import signal
from multiprocessing import Event, Process, Queue
from queue import Empty

from pydispatch import dispatcher
from scrapy import signals
from scrapy.crawler import CrawlerProcess


class CrawlerWorker(Process):
    def __init__(self, settings, return_items, *crawl_args, **crawl_kwargs):
        super().__init__(daemon=True)
        self.settings = settings
        self.result_queue = Queue()
        self.crawl_args = crawl_args
        self.crawl_kwargs = crawl_kwargs

        # Shared across processes.
        self.kill_process = Event()

    def _spider_error(self, failure):
        self.result_queue.put(failure.value)

    def _exit_gracefully(self, signum, frame):
        self.kill_process.set()
        process = getattr(self, "process", None)
        if process is not None:
            process.stop()

    def run(self):
        # Twisted/Scrapy objects must be created in the child process.
        self.process = CrawlerProcess(self.settings)
        dispatcher.connect(self._spider_error, signals.spider_error)
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)

        self.process.crawl(
            *self.crawl_args, **self.crawl_kwargs, result_queue=self.result_queue
        )
        self.process.start()

    def start(self):
        super().start()
        super().join()

        result = []
        # multiprocessing.Queue.empty() is unreliable; drain using get_nowait().
        while True:
            try:
                result.append(self.result_queue.get_nowait())
            except Empty:
                break

        if self.kill_process.is_set():
            raise KeyboardInterrupt
        if len(result) == 1 and isinstance(result[0], Exception):
            raise result[0]
        if not result:
            return None
        return result
