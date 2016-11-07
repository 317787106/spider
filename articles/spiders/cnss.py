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

    name = "cnss"
    
#     classify2url = getSiteEntryUrl(name)
#     xpath = getSiteXpath(name)
    
    def getTotalPage(self,response):
        
        yield Request(response.url, callback=self.getArticleUrl, meta=response.meta, dont_filter=True)
                
    def getArticleUrl(self,response):
        
        meta = response.meta
        article_urls = response.xpath(self.xpath['article_link']).extract()
        #article_urls = response.xpath('//table[@width="610"]//tr/td/a/@href').extract()
        
        if len(article_urls) > 0:
            for url in article_urls:
                url = response.url + url.strip("./")
                
                meta['url'] = url
                if isArticleExist(url) == False:
                    yield Request(url, callback=self.getContent, meta=meta)
    
    def getContent(self,response):

        item = ArticleItem()
        item['url'] = response.meta['url']
        item['classify'] = response.meta['classify']
        item['data_dir'] = response.meta['data_dir']
                    
        titles = response.xpath(self.xpath['title1']).extract()
        #titles = response.xpath(u'//td[contains(text(),"作 者")]/text() | //td[contains(text(),"作者")]/text()').extract()
        if len(titles)>0:
            title = titles[0].replace(" ","")
            m = re.search(u"[(|（]作者[:|：](\S+)[)|）]",title)
            if m:
                author = m.group(1)
                item['author'] = author
               
            index = title.find("(")
            if index!=-1:
                title = title[0:index]
                
            index = title.find("（")
            if index!=-1:
                title = title[0:index]
                
            item['title'] = title
            
        if item.get("title") is None:
            titles = response.xpath(self.xpath['title2']).extract()
            #titles = response.xpath(u'//td[@class="STYLE2"]/text()').extract()
            if len(titles)>0:
                item['title'] = titles[0]
        
        subdata = response.xpath(self.xpath['subdata1']).extract()
        #subdata = response.xpath(u'//div[@class="TRS_Editor"]/div').extract()
        if len(subdata) == 0:
            subdata = response.xpath(self.xpath['subdata2']).extract()
            #subdata = response.xpath(u'//div[@class="TRS_Editor"]').extract()
            
        if len(subdata) > 0:
            contents = Selector(text=subdata[0]).xpath("//text()").extract()
            
            #第一段为摘要
            if len(contents)>=1 and contents[0].find("：") != -1:
                index = contents[0].find("：")
                item['abstract'] = contents[0][index:]
                
            #第二段为关键词
            if len(contents)>=2 and contents[1].find("：")!=-1:
                index = contents[1].find("：")
                item['keywords'] = contents[1][index:]
        
            #print content
            content = self.body_prefix + subdata[0] + self.body_suffix
            
            # md5每次都需要初始化
            m = hashlib.md5()
            m.update(response.url)
            filename = response.meta['data_dir']+m.hexdigest()+".html"
            
            with open(filename,'w') as f:
                f.write(content)
            
            item['content_type'] = 2
            item['content_path'] = filename
        
        yield item
