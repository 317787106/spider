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

    name = "tianjin"
    
    url_pattern = "http://www.tj.lss.gov.cn/ecdomain/portal/portlets/newslist/newslistcomponent.jsp?goPage=1&pageNum=%s&siteID=tj&pageID=mciakmldehicbbodidnlmldmhkighpdn&moduleID=llhglblnkgjkbboejpinpopkpbhedemg&moreURI=/ecdomain/framework/tj/mciakmldehicbbodidnlmldmhkighpdn/llhglblnkgjkbboejpinpopkpbhedemg.do&var_temp=ogeiknkfehicbbodidnlmldmhkighpdn&currfolderid=null&showChildFlag=false&displayPageLinkFlag=true"
    url_prefix = "http://www.tj.lss.gov.cn"
    
    def start_requests(self):
        for i in range(1,102):
            yield Request(self.url_pattern % i,callback=self.parse)
        
    def parse(self,response):
        
        meta = {'data_dir':self.data_dir}
        article_urls = response.xpath('//a[@class="ALink"]/@href').extract()
        
        for url in article_urls:
            if not url.startswith("http:"):

                url = self.url_prefix + url
                
                if isMaterialExist(url) == False:
                    yield Request(url,callback=self.getContent,meta=meta)
                
    def getContent(self,response):
        
        item = MaterialItem()
        
        titles = response.xpath('//td[@class="zwgk_xx_data_title"]/text()').extract()
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
        