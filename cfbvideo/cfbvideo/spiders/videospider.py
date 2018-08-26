# -*- coding: utf-8 -*-
import scrapy


class VideospiderSpider(scrapy.Spider):
    name = 'videospider'
    allowed_domains = ['channelfireball.com']
    start_urls = ['https://www.channelfireball.com/videos/']

    def parse(self, response):
        pass
