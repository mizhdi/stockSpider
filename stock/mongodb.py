import pymongo
from scrapy.conf import settings

def init_mongodb():
    connection = pymongo.MongoClient(
        settings['MONGODB_SERVER'],
        settings['MONGODB_PORT']
    )
    
    db = connection[settings['MONGODB_DB']]
    
    return db
    