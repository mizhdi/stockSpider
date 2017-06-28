# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy import log
from twisted.conch.insults.window import cursor
from stock.mongodb import init_mongodb

class StockPipeline(object):

    def __init__(self):
        self.db = init_mongodb()

    def process_item(self, item, spider):
        if spider.name == 'baiduTopStockSpider':
            collection = self.db[settings['stock']]
            d = dict(item)
            cursor = list(collection.find({'num': d["num"], 'source': d["source"]}))
        
            if cursor:
                collection.update({'_id': cursor[0]['_id']}, d)
            else:
                collection.insert(d)
            log.msg("stock added to MongoDB database!", level=log.DEBUG, spider=spider)
        elif spider.name == 'xueqiuPostSpider':
            collection = self.db['post']
            collection.save(dict(item))
            log.msg("post added to MongoDB database!", level=log.DEBUG, spider=spider)
        
        return item
