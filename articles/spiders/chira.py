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

    name = "chira"
    
    url_prefix = "http://www.chira.org.cn"
    
#     classify2url = getSiteEntryUrl(name)
#     xpath = getSiteXpath(name)
    
    def getTotalPage(self,response):
        
        m = re.search(r"last_page\":(\d+),",response.body)
        if m:
            total_count = m.group(1)
            total_count = int(total_count)
            for i in range(1,total_count+1):
                url = response.url.rstrip("\.html")+"/page/"+str(i)+".html"
                yield Request(url, callback=self.getArticleUrl, meta=response.meta)
                
    def getArticleUrl(self,response):
        
        meta = response.meta
        article_urls = response.xpath(self.xpath["article_link"]).extract()
        #article_urls = response.xpath('(//div[@class="newsList"])//div[@class="title"]/a/@href').extract()
        
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
        
        titles = response.xpath(self.xpath["title"]).extract()
        #titles = response.xpath('//div[@class="newShow"]/div[@class="title"]/text()').extract()
        if len(titles) > 0:
            item['title'] = titles[0].strip()
            
        subdata = response.xpath(self.xpath["head"]).extract()
        #subdata = response.xpath('//div[@class="newShow"]/div[@class="time"]/text()').extract()
        if len(subdata)>0:
            m = re.search(r"(\d{4}-\d{2}-\d{2})",subdata[0])
            if m:
                day = m.group(1)
                item['publish_time'] = day
            
            m = re.search(u"作者：(\S+)\s+",subdata[0])
            if m:
                author = m.group(1)
                item['author'] = author
                
            m = re.search(u"来源：(\S+)\s+",subdata[0])
            if m:
                source = m.group(1)
                item['source'] = source
               
        contents = response.xpath(self.xpath["content"]).extract()
        #contents = response.xpath('//div[@class="newShow"]/div[@class="content"]').extract()
        
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
