# encoding: utf-8

from __future__ import division

import sys

from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.http import Request
from articles.items import ArticleItem
from articles.utils import isArticleExist
from __init__ import MaterialSpider
import urlparse
from urllib import urlencode

import re

class AmazonSpider(MaterialSpider):

    name = "beijing"
                            
    start_urls = [
            "http://www.bjrbj.gov.cn/xxgk/gzdt/index_1.html",
#             "http://www.bjrbj.gov.cn/xxgk/gzdt/index_2.html",
#             "http://www.bjrbj.gov.cn/xxgk/gzdt/index_3.html",
#             "http://www.bjrbj.gov.cn/xxgk/gzdt/index_4.html",
#             "http://www.bjrbj.gov.cn/xxgk/gzdt/index_5.html",
#             "http://www.bjrbj.gov.cn/xxgk/gzdt/index_6.html",
#             "http://www.bjrbj.gov.cn/xxgk/gzdt/index_7.html",
#             "http://www.bjrbj.gov.cn/xxgk/gzdt/index_8.html",
#             "http://www.bjrbj.gov.cn/xxgk/gzdt/index_9.html",
#             "http://www.bjrbj.gov.cn/xxgk/gzdt/index_10.html",
#             "http://www.bjrbj.gov.cn/xxgk/gzdt/index_11.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_1.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_2.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_3.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_4.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_5.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_6.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_7.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_8.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_9.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_10.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_11.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_12.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_13.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_14.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_15.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_16.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_17.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_18.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_19.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_20.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_21.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_22.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_23.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_24.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_25.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_26.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_27.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_28.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_29.html",
#             "http://www.bjrbj.gov.cn/xxgk/gsgg/index_30.html",
#             "http://www.bjrbj.gov.cn/xxgk/zcfg/"
#             "http://www.bjrbj.gov.cn/xxgk/zcfg/index_1.html",
#             "http://www.bjrbj.gov.cn/xxgk/zcfg/index_2.html",
#             "http://www.bjrbj.gov.cn/xxgk/zcjd/"
#             "http://www.bjrbj.gov.cn/xxgk/zcjd/index_1.html",
#             "http://www.bjrbj.gov.cn/xxgk/zcjd/index_2.html"
            ]
    
    def parse(self,response):
        
        article_urls = Selector(text=response.body.decode("gbk")).xpath('//a[contains(@href,"html") and contains(@href,"/t")]/@href').extract()
        
        index = response.url.rfind("/")
        url_prefic = response.url[0:index]
        for url in article_urls[0:1]:
            if not url.startswith("http:"):
                index = url.find("/")
                url = url_prefic + url[index:]
                yield Request(url,callback=self.getContent)
                
    def getContent(self,response):
        print response.url
