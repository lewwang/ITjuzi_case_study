# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    city = scrapy.Field()
    com_claim = scrapy.Field()
    com_history = scrapy.Field()
    com_round = scrapy.Field()
    com_scope = scrapy.Field()
    combo_make_com = scrapy.Field()
    des = scrapy.Field()
    education = scrapy.Field()
    famous_com = scrapy.Field()
    famous_school = scrapy.Field()
    follow_num = scrapy.Field()
    follow_status = scrapy.Field()
    id = scrapy.Field()
    invse_history = scrapy.Field()
    invse_round = scrapy.Field()
    invse_scope = scrapy.Field()
    invst_claim = scrapy.Field()
    invst_history = scrapy.Field()
    job = scrapy.Field()
    location = scrapy.Field()
    logo = scrapy.Field()
    name = scrapy.Field()
    prov = scrapy.Field()
    type = scrapy.Field()
