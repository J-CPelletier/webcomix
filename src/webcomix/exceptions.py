class CrawlerBlocked(Exception):
    pass


class NextLinkNotFound(Exception):
    def __init__(self, failed_url, next_page_xpath):
        self.failed_url = failed_url
        self.next_page_xpath = next_page_xpath
