# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
from taobao.items import TaobaoItem


class SpiderOneSpider(scrapy.Spider):
    name = 'spider_one'
    allowed_domains = ['taobao.com']

    def start_requests(self):
        url = 'https://www.taobao.com/'
        yield Request(url=url, callback=self.get_types_url)

    def get_types_url(self, response):
        result = response.xpath('//li[contains(@class, "J_Cat")]/a/@href').extract()
        L = []
        for items in result:
            url = response.urljoin(items)
            if url not in L:
              L.append(url)
        L.pop(6), L.pop(6), L.pop(16), L.pop(16), L.pop(16)
        for i in L:
            url = i
            yield Request(url=url, callback=self.get_detail_url)

    def get_detail_url(self, response):
        try:
            result = response.xpath('//dd[contains(@class, "cat-title")]/a/@href').extract()
            if result:
                for i in result:
                    url = response.urljoin(i)
                    yield Request(url=url, callback=self.get_product_url)
            else:
                url = response.url
                yield Request(url=url, callback=self.next_parse_url)
        except:
            self.logger.debug('解析网页出错', response.url)

    def next_parse_url(self, response):
        URL = response.url
        try:
            result = response.xpath('//span[@class="sub-link"]/a/@href').extract()
            if result:
                for i in result:
                    url = response.urljoin(i)
                    yield Request(url=url, callback=self.get_product_url)
            else:
                url = response.url
                yield Request(url=url, callback=self.once_parse_url)

        except:
            self.logger.debug('解析网页出错', URL)
    def once_parse_url(self, response):
        URL = response.url
        try:
            result = response.xpath('//div[@class="box-cell-container"]/a/@href').extract()
            if result:
                for i in result:
                    url = response.urljoin(i)
                    yield Request(url=url, callback=self.get_product_url)
            else:
                url = response.url
                yield Request(url=url, callback=self.two_parse_url)

        except:
            self.logger.debug('解析网页出错', URL)

    def two_parse_url(self, response):
        URL = response.url
        try:
            html = response.text
            result = re.findall('{&quot;cat_name&quot;:&quot;(.*?)&quot', html, re.S)
            if result:
                for name in result:
                    url = 'https://s.taobao.com/search?q='
                    urljoin = url + str(name)
                    yield Request(url=urljoin, callback=self.get_product_url)
            else:
                url = response.url
                yield Request(url=url, callback=self.get_product_url)

        except:
            self.logger.debug('解析网页出错', URL)

    def get_product_url(self, response):
        URL = response.url
        try:
            url = response.url
            length = len(response.text)
            if length > 100000:
                for i in range(100):
                    urljoin = url + '&bcoffset=12&s=' + str(i*60)
                    yield Request(url=urljoin, callback=self.get_product)
        except:
            self.logger.debug("解析网页出错", URL)
    def get_product(self, response):
        URL = response.url
        try:
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
            for x in nick:
                item = TaobaoItem()
                item['title'] = title[i]
                item['pic_url'] = pic_url[i]
                item['view_price'] = view_price[i]
                item['view_fee'] = view_fee[i]
                item['item_loc'] = item_loc[i]
                item['view_sales'] = view_sales[i]
                item['nid'] = 'https://item.taobao.com/item.htm?spm=a219r.lm874.14.1.13c42140RGlAs3&id=' + str(nid [i])
                item['nick'] = nick[i]
                i += 1
                yield item
        except:
            self.logger.debug(URL)




















