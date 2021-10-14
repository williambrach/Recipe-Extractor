# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipelinkextractorItem(scrapy.Item):
    title = scrapy.Field()
    csv_path = scrapy.Field()
    dir_path = scrapy.Field()
    links = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
