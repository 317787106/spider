# encoding: utf-8

from __future__ import division

import sys
from __builtin__ import True
reload(sys)
sys.setdefaultencoding("utf-8")

from scrapy import Selector
from scrapy.http import Request
from articles.items import ArticleItem
from articles.utils import isArticleExist

from __init__ import BaseSpider

import re
import hashlib

class AmazonSpider(BaseSpider):
    
    name = "chinajob"
    
    url_prefix = "http://www.chinajob.gov.cn/"
    
    #classify2url = getSiteEntryUrl(name)
    #xpath = getSiteXpath(name)
    
    def getTotalPage(self,response):
        
        meta = response.meta
        #meta['dont_redirect'] = True
        
        article_urls = response.xpath(self.xpath['article_link']).extract()
        #article_urls = response.xpath('//ul[@class="bottom_ul" or @class="news_ul"]/li/a/@href').extract()
        
        if len(article_urls) > 0:
            for url in article_urls:
                if url.startswith("../"):
                    url = self.url_prefix + url.strip("../")
                    
                if not url.startswith("http://"):
                    index = response.url.rfind("/")
                    url = response.url[0:index+1]+url
                    
                meta['url'] = url
                if isArticleExist(url) == False:
                    yield Request(url, callback=self.getContent, meta=meta)
                    return
        
        next_page_urls = response.xpath(self.xpath['next_page_link']).extract()     
        #next_page_urls = response.xpath('//div[@id="displaypagenum"]//a[contains(text(),">>")]/@href').extract()
        if len(next_page_urls) > 0:
            index = response.url.rfind("/")
            next_page_url = response.url[0:index+1]+ next_page_urls[0]
#             print next_page_url
            yield Request(next_page_url, callback=self.getTotalPage, meta=meta)
    
    def getContent(self,response):
        
        item = ArticleItem()
        item['url'] = response.meta['url']
        item['classify'] = response.meta['classify']
        item['data_dir'] = response.meta['data_dir']
                
        titles = response.xpath(self.xpath['title']).extract()    
        #titles = response.xpath(u'//div[@class="content_title"]/h1/text()').extract()
        if len(titles)>0:
            item['title'] = titles[0].strip()
            
        source = response.xpath(self.xpath['source']).extract()
        #source = response.xpath(u'//div[@class="content_top"]/span[@class="from"]/text()').extract()
        if len(source)>0:
            data = source[0].strip()
            index = data.find("：")
            if index != -1:
                item['source'] = data[index+1:]
            else:
                item['source'] = data
            
        publish_time = response.xpath(self.xpath['publish_time']).extract()
        #publish_time = response.xpath(u'//div[@class="content_top"]/span[@class="time"]/text()').extract()
        if len(publish_time)>0:
            data = publish_time[0].strip()
            index = data.find("：")
            if index != -1:
                item['publish_time'] = data[index+1:]
            else:
                item['publish_time'] = data
            
        content = response.xpath(self.xpath['content']).extract()
        #content = response.xpath(u'//div[@id="content_content"]').extract()

        if len(content) > 0:
        
            content = self.body_prefix + content[0] + self.body_suffix
            
            # md5每次都需要初始化
            m = hashlib.md5()
            m.update(response.url)
            filename = response.meta['data_dir']+m.hexdigest()+".html"
            
            with open(filename,'w') as f:
                f.write(content)
            
            item['content_type'] = 2
            item['content_path'] = filename
        
        yield item
