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

    name = "hangzhou"
                            
    start_urls = [
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/zhl/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/zhl/index2.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/zhl/index3.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/zhl/index4.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/rsrc/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/rsrc/index2.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/rsrc/index3.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/rsrc/index4.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/jyyzjy/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/jyyzjy/index2.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/jyyzjy/index3.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/jyyzjy/index4.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/jyyzjy/index5.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/jyyzjy/index6.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/jyyzjy/index7.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/pxjnjd/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/pxjnjd/index2.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/pxjnjd/index3.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/pxjnjd/index4.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/pxjnjd/index5.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/pxjnjd/index6.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/pxjnjd/index7.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ldlgl/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ldlgl/index2.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index2.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index3.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index4.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index5.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index6.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index7.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index8.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index9.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index10.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index11.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index12.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index13.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index14.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index15.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gzfu/index16.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ldbh/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index2.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index3.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index4.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index5.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index6.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index7.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index8.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index9.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index10.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index11.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index12.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index13.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx/index14.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index2.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index3.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index4.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index5.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index6.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index7.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index8.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index9.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index10.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index11.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index12.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index13.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index14.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index15.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index16.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index17.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index18.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index19.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ylbx2/index20.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/sybx/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/sybx/index2.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/sybx/index3.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gsbx/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gsbx/index2.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/gsbx/index3.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/shybx/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/ldzyzc/index.html",
            "http://www.zjhz.lss.gov.cn/html/zcfg/zcfgk/qtldfg/index.html",
            ]
    
    url_prefix = "http://www.zjhz.lss.gov.cn"
    
    def parse(self,response):
        
        meta = {'data_dir':self.data_dir}
        a_links = Selector(text=response.body.decode("gbk")).xpath('//div[@class="tupianxinwenleftcon1 tupianxinwenleftcon_w"]//ul/li/a').extract()
        
        for a_link in a_links:
            urls = Selector(text=a_link).xpath('//a/@href').extract()
            titles = Selector(text=a_link).xpath('//a/text()').extract()
            if len(urls)>0 and len(titles)>0:
                url = urls[0]
                meta['title'] = titles[0]
                
                if not url.startswith("http:"):
    
                    url = self.url_prefix + url
                    
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
        item["title"] = response.meta['title']
        item["classify"] = self.name
        item["content_path"] = filename
        
        yield item
        