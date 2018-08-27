# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import unicodedata
from datetime import datetime


class VideospiderSpider(scrapy.Spider):
    name = 'videospider'
    allowed_domains = ['channelfireball.com']
    start_urls = ['https://www.channelfireball.com/videos/']


    def parse(self, response):
        videos_urls = response.xpath('////*[@class="postTitle"]//a/@href').extract()
        print(videos_urls)
        for video_url in videos_urls:
            yield Request(video_url, callback = self.parse_video)

        next_page = response.xpath('//*[@class="next page-numbers"]/@href').extract_first()
        yield Request(next_page, callback = self.parse)



    def parse_video(self, response):
        head_data = response.xpath('//*[@class="postTitle"]')[0]
        head_data_list = head_data.xpath('.//text()')

        title = head_data_list[0].extract()
        author = head_data_list[2].extract()
        date = head_data_list[3].extract()
        date = self.transform_to_datetime(date)

        page_url = response.request.url
        youtube_url = response.xpath('//*[@class="wp-video-shortcode"]//@src').extract_first()

        avatar_url = response.xpath('//*[@class="gravatar"]//@src').extract_first()

        bio_node = response.xpath('//*[@class="about"]//child::*')[2]
        bio = bio_node.xpath('.//text()').extract_first()
        bio = unicodedata.normalize("NFKD", bio)

        tags = response.xpath('//*[@rel="tag"]//text()').extract()

        yield {
                "title": title,
                "author": author,
                "date": date,
                "page_url": page_url,
                "youtube_url": youtube_url,
                "avatar_url": avatar_url,
                "bio": bio,
                "tags": tags,
        }

    def transform_to_datetime(self, date_str):
        date = unicodedata.normalize("NFKD", date_str)
        date = date.replace("  //  ","")
        date = date.replace(",","")
        return datetime.strptime(date, "%d %b %Y").utcnow()
