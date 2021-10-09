# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NaverItem(scrapy.Item):
    text = scrapy.Field()
    key = scrapy.Field()
    url = scrapy.Field()
    rank = scrapy.Field()
    img_url = scrapy.Field()
    related = scrapy.Field()
    