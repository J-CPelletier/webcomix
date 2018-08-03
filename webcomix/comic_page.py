import scrapy


class ComicPage(scrapy.Item):
    url = scrapy.Field()
    page = scrapy.Field()
