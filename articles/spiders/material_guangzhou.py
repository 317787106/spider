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

    name = "guangzhou"
                            
    start_urls = [
            "http://www.hrssgz.gov.cn/zcfg/index.html",
            "http://www.hrssgz.gov.cn/zcfg/index_1.html",
            "http://www.hrssgz.gov.cn/zcfg/index_2.html",
            "http://www.hrssgz.gov.cn/zcfg/index_3.html",
            "http://www.hrssgz.gov.cn/zcfg/index_4.html",
            "http://www.hrssgz.gov.cn/zcfg/index_5.html",
            "http://www.hrssgz.gov.cn/zcfg/index_6.html",
            "http://www.hrssgz.gov.cn/zcfg/index_7.html",
            "http://www.hrssgz.gov.cn/zcfg/index_8.html",
            "http://www.hrssgz.gov.cn/zcfg/index_9.html",
            "http://www.hrssgz.gov.cn/zcfg/index_10.html",
            "http://www.hrssgz.gov.cn/zcfg/index_11.html",
            "http://www.hrssgz.gov.cn/zcfg/index_12.html",
            "http://www.hrssgz.gov.cn/zcfg/index_13.html",
            "http://www.hrssgz.gov.cn/zcfg/index_14.html",
            "http://www.hrssgz.gov.cn/zcfg/index_15.html",
            "http://www.hrssgz.gov.cn/zcfg/index_16.html",
            "http://www.hrssgz.gov.cn/zcfg/index_17.html",
            "http://www.hrssgz.gov.cn/zcfg/index_18.html",
            "http://www.hrssgz.gov.cn/zcfg/index_19.html",
            "http://www.hrssgz.gov.cn/zcfg/index_20.html",
            "http://www.hrssgz.gov.cn/zcfg/index_21.html",
            "http://www.hrssgz.gov.cn/zcfg/index_22.html",
            "http://www.hrssgz.gov.cn/zcfg/index_23.html",
            "http://www.hrssgz.gov.cn/zcfg/index_24.html",
            ]
    
    def parse(self,response):
        
        meta = {'data_dir':self.data_dir}
        a_links = Selector(text=response.body.decode("gbk")).xpath('//a[@class="rsjfont8" and contains(@href,"t")]').extract()
        
        index = response.url.rfind("/")
        url_prefix = response.url[0:index]
        for a_link in a_links:
            urls = Selector(text=a_link).xpath('//a/@href').extract()
            titles = Selector(text=a_link).xpath('//a/text()').extract()
            if len(urls)>0 and len(titles)>0:
                url = urls[0]
                meta['title'] = titles[0]
                
                if not url.startswith("http:"):
                    index = url.find("/")
                    url = url_prefix + url[index:]
                    
                    if isMaterialExist(url) == False:
                        yield Request(url,callback=self.getContent,meta=meta)
                
    def getContent(self,response):
        
        item = MaterialItem()
        
        #写入文件
        # md5每次都需要初始化
        m = hashlib.md5()
        m.update(response.url)
        filename = response.meta['data_dir']+m.hexdigest()+".html"
        fp = open(filename,'w')
        fp.write(response.body)
        fp.close()
        
        item["url"] = response.url
        item["title"] = response.meta["title"]
        item["classify"] = self.name
        item["content_path"] = filename
        
        yield item
        