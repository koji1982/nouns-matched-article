import scrapy

class ArticleItem(scrapy.Item):
    url = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    noun = scrapy.Field()
