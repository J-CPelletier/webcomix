import scrapy


class ComicPage(scrapy.Item):
    image_element = scrapy.Field()
    page = scrapy.Field()
