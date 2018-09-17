# -*- coding: utf-8 -*-
import scrapy
import re
from taobao.items import TaobaoItem
class TextSpider(scrapy.Spider):
    name = 'text'
    allowed_domains = ['taobao.com/markets/amusement/home']
    start_urls = ['https://s.taobao.com/list?q=%E6%AF%9B%E8%A1%A3&cat=16&style=grid&seller_type=taobao&spm=a217f.8051907.1000187.1']

    def parse(self, response):

        URL = response.url

        html = response.text
        title = re.findall('"raw_title":"(.*?)"', html, re.S)
        pic_url = re.findall('"pic_url":"(.*?)"', html, re.S)
        view_price = re.findall('"view_price":"(.*?)"', html, re.S)
        view_fee = re.findall('"view_fee":"(.*?)"', html, re.S)
        item_loc = re.findall('"item_loc":"(.*?)"', html, re.S)
        view_sales = re.findall('"view_sales":"(.*?)"', html, re.S)
        nid = re.findall('"nid":"(.*?)"', html, re.S)
        nick = re.findall('"nick":"(.*?)"', html, re.S)
        nick.pop(-1)
        i = 0
        for x in view_price:
            item = TaobaoItem()
            item['title'] = title[i]
            print(title[i])
            item['pic_url'] = pic_url[i]
            item['view_price'] = view_price[i]
            item['view_fee'] = view_fee[i]
            item['item_loc'] = item_loc[i]
            item['view_sales'] = view_sales[i]
            item['nid'] = 'https://item.taobao.com/item.htm?spm=a219r.lm874.14.1.13c42140RGlAs3&id=' + str(nid[i])
            item['nick'] = nick[i]
            i += 1
            print(item)
            yield item


