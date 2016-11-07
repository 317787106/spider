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

    name = "drcnet"
    
#     classify2url = getSiteEntryUrl(name)
#     xpath = getSiteXpath(name)
        
    def getTotalPage(self,response):
        print response.url
        
        pages = response.xpath(self.xpath["page_link"]).extract()
        #pages = response.xpath('//span[@id="ContentPlaceHolder1_MainMiddleControl1_WebPageDocumentsByUId1_span_totalpage"]/text()').extract()
        
        urls = []
        if len(pages) > 0:
            total_count = int(pages[0])
            
            for i in range(1,int(total_count)):
            #for i in range(1,2):
                urls.append(response.url +"&curpage=%s" % i)
        
        for url in urls:
            yield Request(url, callback=self.getArticleUrl, meta=response.meta)
                
    def getArticleUrl(self,response):
                
        article_urls = response.xpath(self.xpath["article_link"]).extract()
        #article_urls = response.xpath('//ul[@id="ContentPlaceHolder1_MainMiddleControl1_WebPageDocumentsByUId1"]/li/div[@class="m_sub"]/a/@href').extract()
        
        if len(article_urls) > 0:
            for url in article_urls:
                
                if not url.startswith("http://"):
                    continue
                
                if isArticleExist(url) == False:
                    yield Request(url, callback=self.getContent, meta=response.meta)
    
    #收费登录
    def getContent(self,response):
        meta = response.meta
        
        subdata = response.xpath(self.xpath["subdata"]).extract()
        #subdata = response.xpath('//div[@id="disArea"]').extract()
        if len(subdata)==0:
            return
        
        item = ArticleItem()
        item['url'] = response.url
        item['classify'] = meta['classify']
        item['data_dir'] = meta['data_dir']
        
        contents = Selector(text=subdata[0])
        
        item['title'] = "".join(contents.xpath(self.xpath["title"]).extract())
        #item['title'] = "".join(contents.xpath('//div[@id="docSubject"]//text()').extract())
        
        publish_time = contents.xpath(self.xpath["publish_time"]).extract()
        #publish_time = contents.xpath('//div[@id="docDeliveddate"]//text()').extract()
        if len(publish_time)>0:
            item['publish_time'] = publish_time[0]
        
        abstraces = contents.xpath(self.xpath["abstract"]).extract()
        #abstraces = contents.xpath('//div[@id="docSummary"]//text()').extract()
        for abstract in abstraces:
            if len(abstract) > 5:
                item['abstract'] = abstract.strip()
        
        keywords = contents.xpath(self.xpath["keywords"]).extract()
        #keywords = contents.xpath('(//div[@id="docKeywords"]//text())[2]').extract()
        if len(keywords)>0:
            item['keywords'] = keywords[0].strip()
            
        author = contents.xpath(self.xpath["author"]).extract()
        #author = contents.xpath('(//span[@id="docAuthor"]//text())[2]').extract()
        if len(author)>0:
            item['author'] = author[0].strip()
            
        source = contents.xpath(self.xpath["source"]).extract()
        #source = contents.xpath('(//span[@id="docSource"]//text())[2]').extract()
        if len(source)>0:
            item['source'] = source[0].strip()
            
        content = contents.xpath(self.xpath["content"]).extract()
        #content = contents.xpath('//div[@id="docContent"]').extract()
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