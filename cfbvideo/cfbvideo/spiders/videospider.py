# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class VideospiderSpider(scrapy.Spider):
    name = 'videospider'
    allowed_domains = ['channelfireball.com']
    start_urls = ['https://www.channelfireball.com/videos/']

    def parse(self, response):
        videos_urls = response.xpath('////*[@class="postTitle"]//a/@href').extract()
        for video_url in videos_urls:
            yield Request(video_url, callback= self.parse_video)

    def parse_video(self, response):
        pass
