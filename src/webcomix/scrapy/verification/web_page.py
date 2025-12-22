import scrapy


class WebPage(scrapy.Item):
    url = scrapy.Field()
    page = scrapy.Field()
    image_urls = scrapy.Field()
    alt_text = scrapy.Field()
