import requests
import json
import redis
import logging
from .settings import REDIS_URL
from random import choice
from scrapy.conf import settings

reds = redis.Redis.from_url(REDIS_URL, db=2, decode_responses=True)
login_url = 'https://xueqiu.com'

def get_cookie():
#     request and get cookie
#     return '{"xq_a_token": "0a52c567442f1fdd8b09c27e0abb26438e274a7e","xq_r_token": "43c6fed2d6b5cc8bc38cc9694c6c1cf121d38471"}';
    headers = {'User-Agent': choice(settings["USER_AGENT_CHOICES"])}
    r = requests.get(login_url, headers=headers)
    cookies = r.cookies.get_dict()
    
    return json.dumps(cookies)
            
def init_cookie(spidername):
    if reds.get("%s:Cookies" % (spidername)) is None:
        cookie = get_cookie()
        reds.set("%s:Cookies" % (spidername), cookie)
    
def update_cookie():
    pass

def delete_cookie():
    pass