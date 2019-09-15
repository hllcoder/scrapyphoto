# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re
from scrapy.http import Request


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        name = item.get('name')
        for url in item['img_url']:
            yield Request(url, meta={'name': name},headers={'referer':item['refer']})

    def file_path(self, request, response=None, info=None):
        name = request.meta.get('name')
        name = re.sub(r'[？\\*|“<>:/()0123456789]', '', name)
        image_guid = request.url.split('/')[-1]
        filename = u'/{0}/{1}'.format(name, image_guid)
        return filename

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['img_url'] = image_path
        return item
