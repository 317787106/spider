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
    
    name = "exuezhe"
    
    url_prefix = "http://ipub.exuezhe.com/qkpaper.html?id="
    
    def getTotalPage(self,response):
        
        meta = response.meta
        #meta['dont_redirect'] = True
        index = response.url.find("=")
        if index != -1:
            classify = response.url[index+1:]
            
            meta["classify"] = classify
            url = "http://ipub.exuezhe.com/Qk/GetAllYear/%s" % classify
            
            yield Request(url, callback=self.getAllYear, meta=meta)
        
    def getAllYear(self,response):
        meta = response.meta
        
        data = response.body.strip("[").strip("]").split(",")
        data = [item.strip('"') for item in data]
        
        for year in data:
            meta["year"] = year
            url = "http://ipub.exuezhe.com/Qk/GetNoByYear?dh=%s&nf=%s" % (meta["classify"],year)
            
            yield Request(url, callback=self.getAllMonth, meta=meta)
    
    
    def getAllMonth(self,response):
        meta = response.meta
        
        data = response.body.strip("[").strip("]").split(",")
        data = [item.strip('"') for item in data]        
        
        for month in data:
            meta["month"] = month
            
            url = "http://ipub.exuezhe.com/Qk/GetArtList?dh=%s&nf=%s&qh=%s&ps=24&pn=1" % (meta["classify"],meta["year"],month)
            
            yield Request(url, callback=self.getArticlesID, meta=meta)
        
    def getArticlesID(self,response):
        meta = response.meta
        
        article_ids = response.xpath(self.xpath["article_id"]).extract()
        #article_ids = response.xpath('//d/r1/id/text()').extract()
        
        for article_id in article_ids:
            
            article_url = self.url_prefix + article_id
            
            if isArticleExist(article_url) == False:
            
                url = "http://ipub.exuezhe.com/Qk/GetTextArt?id=%s&pn=1&ps=100" % article_id
                
                meta["url"] = article_url
                meta["article_id"] = article_id
                
                yield Request(url, callback=self.getContent, meta=meta)
        

    def getContent(self,response):
        meta = response.meta
        
        content = self.body_prefix + "<div>" + response.body + "</div>" + self.body_suffix
        
        # md5每次都需要初始化
        m = hashlib.md5()
        m.update(response.url)
        filename = response.meta['data_dir']+m.hexdigest()+".html"
        
        with open(filename,'w') as f:
            f.write(content)
        
        meta['content_type'] = 2
        meta['content_path'] = filename
        
        url = "http://ipub.exuezhe.com/Qw/GetBaseArt?id=" + meta["article_id"]
        
        yield Request(url, callback=self.getSubdata, meta=meta)
            
    def getSubdata(self,response):
        
        item = ArticleItem()
        item['url'] = response.meta['url']
        item['classify'] = response.meta['classify']
        item['data_dir'] = response.meta['data_dir']
        item['content_type'] = response.meta['content_type']
        item['content'] = response.meta['content']
        
        titles = response.xpath(self.xpath["title"]).extract()
        #titles = response.xpath(u'//d/r1/til/text()').extract()
        if len(titles)>0:
            item['title'] = titles[0].strip()
        
        authors = response.xpath(self.xpath["author"]).extract()
        #authors = response.xpath(u'//d/r1/stil/aut/text()').extract()
        if len(authors)>0:
            item['author'] = authors[0].strip()
            
        sources = response.xpath(self.xpath["source"]).extract()
        #sources = response.xpath(u'//d/r1/stil/taut/opc/text()').extract()
        if len(sources)>0:
            item['source'] = sources[0].strip()
            
        abstracts = response.xpath(self.xpath["abstract"]).extract()
        #abstracts = response.xpath(u'//d/r1/stil/taut/oad/ast/text()').extract()
        if len(abstracts)>0:
            item['abstract'] = abstracts[0].strip()
        
        keywords = response.xpath(self.xpath["keywords"]).extract()
        #keywords = response.xpath(u'//d/r1/stil/taut/oad/kew/text()').extract()
        if len(keywords)>0:
            item['keywords'] = keywords[0].strip()
            
        years = response.xpath(self.xpath["year"]).extract()
        #years = response.xpath(u'//d/r1/stil/taut/oad/py/text()').extract()
        if len(years)>0:
            year = years[0].strip()
            
            months = response.xpath(self.xpath["month"]).extract()
            #months = response.xpath(u'//d/r1/stil/taut/oad/pno/text()').extract()
            if len(months)>0:
                month = months[0].strip()
                
                item['publish_time'] = "%s-%s-01" % (year,month)
    
        yield item