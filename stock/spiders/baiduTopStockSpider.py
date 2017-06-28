import scrapy
from scrapy.selector import Selector
from stock.items import TopStockItem

class baiduTopStockSpider(scrapy.spiders.Spider):
    name = "baiduTopStockSpider"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://top.baidu.com/buzz?b=276&c=17&fr=topbuzz_b277_c17",
    ]
    url = 'http://top.baidu.com'

    def parse(self, response):
        # print(response, type(response))
        # from scrapy.http.response.html import HtmlResponse
        item = TopStockItem()
        selector = Selector(response)
        stocks = selector.xpath('//td[@class="keyword"]/a[@class="list-title"]')

        for index, stock in enumerate(stocks):
            item['name'] = stock.xpath('text()').extract()[0]
            item['num'] = index + 1
            item['source'] = "baidu"
            
            yield item
