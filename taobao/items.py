# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class TaobaoItem(Item):

    # define the fields for your item here like:
    title = Field()
    pic_url = Field()
    view_price = Field()
    view_fee = Field()
    item_loc = Field()
    view_sales = Field()
    url = Field()
    nid = Field()
    nick = Field()



