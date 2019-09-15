# -*- coding: utf-8 -*-
import scrapy
from photos.items import PhotosItem


class TupianSpider(scrapy.Spider):
    name = 'tupian'
    # allowed_domains = ['xx.com']
    start_urls = ['http://www.mm131.net/xinggan/',
				]

    def parse(self, response):
        lis = response.css(".list-left dd:not(.page)")
        for li in lis:
            img_url = li.css("a::attr(href)").extract_first()
            # next_url = response.css(".page-en:nth-last-child(2)::attr(href)").extract_first()
            # if next_url is not None :
            #     yield response.follow(next_url, callback=self.parse)
            yield scrapy.Request(img_url, callback=self.page)

    def page(self, response):
        item = PhotosItem()
        item['name'] = response.css(".content h5::text").extract_first()
        img = response.css(".content-pic img::attr(src)").extract()
        item['img_url'] = img
        item['refer'] = response.url
        yield item
        next_page = response.css(".page-ch:last-child::attr(href)").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.page,dont_filter=True)
