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
                            
    start_urls = [
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_1.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_2.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_3.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_4.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_5.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_6.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_7.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_8.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_9.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_10.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_11.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_12.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_13.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_14.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_15.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_16.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_17.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_18.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_19.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_20.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_21.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_22.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_23.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_24.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_25.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_26.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_27.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_28.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_29.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_30.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_31.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_32.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_33.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_34.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_35.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_36.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_37.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_38.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_39.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_40.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_41.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_42.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_43.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_44.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_45.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_46.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_47.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_48.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_49.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_50.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_51.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_52.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_53.shtml",
            "http://www.12333sh.gov.cn/201412333/xxgk/flfg/gfxwj/index_54.shtml",

            ]
    
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
        