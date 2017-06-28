# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from .cookies import init_cookie, update_cookie
import redis
from random import choice
from scrapy.exceptions import NotConfigured
import json

class CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)
        self.reds = redis.Redis.from_url(settings['REDIS_URL'], db=2, decode_responses=True)
        init_cookie(crawler.spider.name)
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)
    
    def process_request(self, request, spider):
        redisKeys = self.reds.keys()
        while len(redisKeys) > 0:
            if spider.name + ':Cookies' in redisKeys:
                try:
                    cookie = json.loads(self.reds.get(spider.name + ':Cookies'))
                    request.cookies = cookie
                except:
                    print "json string convert to dict failed"
                break
            else:
                pass
                #redisKeys.remove(elem)


class UserAgentMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    
    def __init__(self, user_agents):
        self.enabled = False
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
        user_agents = crawler.settings.get('USER_AGENT_CHOICES', [])

        if not user_agents:
            raise NotConfigured("USER_AGENT_CHOICES not set or empty")

        o = cls(user_agents)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        
        return o

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        self.enabled = getattr(spider, 'rotate_user_agent', self.enabled)
        
    def process_request(self, request, spider):
        if not self.enabled or not self.user_agents:
            return
        request.headers['user-agent'] = choice(self.user_agents) 
