# encoding: utf-8

from __future__ import division

import sys

from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.http import Request
from articles.items import MaterialItem
from articles.utils import isMaterialExist
from __init__ import MaterialSpider
import urlparse
from urllib import urlencode

import re
import hashlib

class AmazonSpider(MaterialSpider):

    name = "shanghai"
                            
    start_urls = ["http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_%s.shtml" % page for page in range(1,24)]
    
    def parse(self,response):
        
        meta = {'data_dir':self.data_dir}
        article_urls = Selector(text=response.body.decode("gbk")).xpath('//a[contains(@href,"shtml") and contains(@href,"/t")]/@href').extract()
        
        index = response.url.rfind("/")
        url_prefix = response.url[0:index]
        for url in article_urls:
            if not url.startswith("http:"):
                index = url.find("/")
                url = url_prefix + url[index:]
                
                if isMaterialExist(url) == False:
                    yield Request(url,callback=self.getContent,meta=meta)
                
    def getContent(self,response):
        
        item = MaterialItem()
        
        titles = Selector(text=response.body.decode("gbk")).xpath('//span[@class="STYLE7"]/text()').extract()
        if len(titles) > 0:
            item["title"] = titles[0]
        
        #写入文件
        # md5每次都需要初始化
        m = hashlib.md5()
        m.update(response.url)
        filename = response.meta['data_dir']+m.hexdigest()+".html"
        fp = open(filename,'w')
        fp.write(response.body)
        fp.close()
        
        item["url"] = response.url
        item["classify"] = self.name
        item["content_path"] = filename
        
        yield item
        