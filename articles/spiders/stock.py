# encoding: utf-8

from __future__ import division

from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider

class AmazonSpider(CrawlSpider):

    name = "stock"
    
    url_prefix = "http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code="

    def start_requests(self):
        
        with open("code/shanghai_code.txt") as f:
            for line in f:
                items = line.strip().split()
                name = items[0]
                code = items[1]
                
                url = self.url_prefix+"sh"+code
                
                meta = {"name":name,"code":code}
                yield Request(url, callback=self.getStockDetail, meta=meta)
                
        with open("code/shenzhen_code.txt") as f:
            for line in f:
                items = line.strip().split()
                name = items[0]
                code = items[1]
                
                url = self.url_prefix+"sz"+code
                
                meta = {"name":name,"code":code}
                yield Request(url, callback=self.getStockDetail, meta=meta)
                
    def getStockDetail(self,response):
        
        fp = open("code/stockholder.txt","a")
        meta = response.meta
        stockholder_nums = response.xpath('//table[@id="Table0"]//tr[2]/td/text()').extract()
        
        content = [meta["name"],meta["code"]]
        if len(stockholder_nums)>0:
            content.extend(stockholder_nums)
            fp.write("\t".join(content)+"\n")