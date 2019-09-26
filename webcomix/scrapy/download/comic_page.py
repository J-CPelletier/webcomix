import scrapy


class ComicPage(scrapy.Item):
    url = scrapy.Field()
    page = scrapy.Field()
    alt_text = scrapy.Field()
