import scrapy
import urlparse
from scrapy.selector import Selector
import json
from scrapy import log
from scrapy.http import Request,FormRequest
from stock.items import PostItem

class xueqiuPostSpider(scrapy.spiders.Spider):
    name = "xueqiuPostSpider"
    rotate_user_agent = True
    allowed_domains = ["xueqiu.com"]
    start_urls = ["https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=-1&count=10&category=-1"]
    
    def __init__(self):
        self.headers = {}
        self.cookies = {}
    
    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, 
                              meta = {'cookiejar': i}, 
                              headers = self.headers, 
                              cookies = self.cookies,
                              callback = self.parse,
                              dont_filter = True)#jump to login page
            
    def parse(self, response):
#         print(response.text, type(response))
        # from scrapy.http.response.html import HtmlResponse
                
        for list in json.loads(response.text)['list']:
            dict = json.loads(list['data'])
            detail_url = "https://xueqiu.com/" + str(dict['user']['id']) + '/' + str(dict['id'])
            
            yield Request(detail_url, callback=self.parse_detail, headers=self.headers, cookies=self.cookies)
            
        url = "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=" + str(json.loads(response.text)['next_max_id']) + "&count=10&category=-1"
        
        yield Request(url, callback=self.parse, headers=self.headers, cookies=self.cookies)
        
        
    def parse_detail(self, response):
        url = urlparse.urlparse(response.url)
        path = url.path.split("/")
        
        item = PostItem()
        selector = Selector(response)
        
        item['postId'] = path[2]
        item['authorId'] = path[1]
        item['postDetail'] = selector.xpath('//div[@class="detail"]').extract()[0]
        
        yield item
        
        
        
        
        