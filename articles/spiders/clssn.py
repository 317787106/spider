# encoding: utf-8

from __future__ import division

import sys
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

    name = "clssn"
    
    url_prefix = "http://www.clssn.com"
    
#     classify2url = getSiteEntryUrl(name)
#     xpath = getSiteXpath(name)
    
    def getTotalPage(self,response):
        meta=response.meta
        
        last_pages = response.xpath(self.xpath['page_link']).extract()
        #last_pages = response.xpath('//a[@id="CBLast"]/@href').extract()
        
        if len(last_pages) > 0:
            total_count = self.getPageNo(last_pages[0])
            
            if total_count > 0:
                index1 = response.url.find("-")
                index2 = response.url.find(".htm")
                for i in range(1,int(total_count)):
                    url = response.url[0:index1+1]+str(i)+response.url[index2:]
                    meta['page_no'] = i

                    yield Request(url, callback=self.getArticleUrl, meta=response.meta)
            
    def getPageNo(self,url):
        index1 = url.find("-")
        index2 = url.find(".htm")
            
        if index1 != -1 and index2 != -1:
            pageno = int(url[index1+1:index2])
            return pageno
        
        return 0
                
    def getArticleUrl(self,response):
        
        meta = response.meta
        
        #跳转后的页面
        current_page_no = self.getPageNo(response.url)
        if current_page_no != meta['page_no']:
            yield Request(response.url,callback=self.getTotalPage,meta=response.meta)
        
        article_urls = response.xpath(self.xpath['article_link']).extract()
        #article_urls = response.xpath('//div[@id="Content1"]/div[@class="xin"]/ul/li/span/a/@href').extract()
        
        #print response.url, len(article_urls)
        
        if len(article_urls) > 0:
            for url in article_urls:
                url = self.url_prefix + url
                
                meta['url'] = url
                if isArticleExist(url) == False:
                    yield Request(url, callback=self.getContent, meta=meta)
    
    def getContent(self,response):

        item = ArticleItem()
        item['url'] = response.meta['url']
        item['classify'] = response.meta['classify']
        item['data_dir'] = response.meta['data_dir']
        
        title = response.xpath(self.xpath['title']).extract()
        #title = response.xpath('//div[@id="Content1"]//span[@id="ReportIDname"]/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
            
        source = response.xpath(self.xpath['source']).extract()
        #source = response.xpath('//div[@id="Content1"]//span[@id="ReportIDMediaName"]/text()').extract()
        if len(source) > 0:
            item['source'] = source[0].strip()
            
        author = response.xpath(self.xpath['author']).extract()
        #author = response.xpath('//div[@id="Content1"]//span[@id="ReportIDgetAuthor"]/text()').extract()
        if len(author) > 0:
            item['author'] = author[0].strip()
            
        publish_time = response.xpath(self.xpath['publish_time']).extract()
        #publish_time = response.xpath('//div[@id="Content1"]//span[@id="ReportIDIssueTime"]/text()').extract()
        if len(publish_time) > 0:
            item['publish_time'] = publish_time[0].strip()
            
        abstract = response.xpath(self.xpath['abstract']).extract()
        #abstract = response.xpath('//div[@id="Content1"]//div[@id="daodu"]/span/text()').extract()
        if len(abstract) > 0:
            item['abstract'] = abstract[0].strip()
            
        contents = response.xpath(self.xpath['content']).extract()   
        #contents = response.xpath('//div[@id="Content1"]//span[@id="ReportIDtext"]').extract()
        
        if len(contents)>0:
            
            content = contents[0].encode("utf-8")
            content = self.body_prefix + content + self.body_suffix
            
            # md5每次都需要初始化
            m = hashlib.md5()
            m.update(response.url)
            filename = response.meta['data_dir']+m.hexdigest()+".html"
            
            with open(filename,'w') as f:
                f.write(content)
            
            item['content_type'] = 2
            item['content_path'] = filename

        yield item
