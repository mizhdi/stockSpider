# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TopStockItem(scrapy.Item):
    # define the fields for your item here like:
    num = scrapy.Field()
    name = scrapy.Field()
    source = scrapy.Field()
    
    pass

class PostItem(scrapy.Item):
    # define the fields for your item here like:
    authorId = scrapy.Field()
    viewCount = scrapy.Field()
    postId = scrapy.Field()
    postTitle = scrapy.Field()
    postDetail = scrapy.Field()

    pass
