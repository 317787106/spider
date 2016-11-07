# encoding: utf-8

from __future__ import division

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.http import Request
from articles.items import ArticleItem
from articles.utils import isArticleExist
from __init__ import BaseSpider
import urlparse
from urllib import urlencode

import re
import hashlib

class AmazonSpider(BaseSpider):

    name = "labournet"
    
    url_prefix1 = "http://www.labournet.com.cn/other/ld_history_jianghua/"
    url_prefix2 = "http://www.labournet.com.cn/lilun/"
    
#     classify2url = getSiteEntryUrl(name)
#     xpath = getSiteXpath(name)
                            
    def getTotalPage(self,response):
        
        article_urls = Selector(text=response.body.decode("gbk")).xpath(self.xpath["article_link"]).extract()
        #article_urls = Selector(text=response.body.decode("gbk")).xpath('//td[@class="unnamed1"]/a[contains(@href,"fileview")]/@href').extract()
        
        if len(article_urls) > 0:

            for url in article_urls:

                result = urlparse.urlparse(url)
                params = urlparse.parse_qs(result.query,True)
                
                meta=response.meta
                meta['title'] = str(params['title'][0]) if "title" in params else ""
                meta['author'] = str(params['name'][0]) if "name" in params else ""
                if "date" in params:
                    date_str = str(params['date'][0])
                    meta['publish_time'] = '%s-%s-%s' % (date_str[0:4],date_str[4:6],date_str[6:8])
                
                if response.url.find("ld_history_jianghua") != -1:
                    meta['url'] = self.url_prefix1 + url
                    url = self.url_prefix1 + url.encode("gbk")
                else:
                    meta['url'] = self.url_prefix2 + url
                    url = self.url_prefix2 + url.encode("gbk")
                
                if isArticleExist(url) == False:
                    yield Request(url, callback=self.getContent, meta=meta)
    
    def getContent(self,response):
        
        meta = response.meta
        
        item = ArticleItem()
        item['url'] = meta['url']
        
        item['classify'] = response.meta['classify']
        item['data_dir'] = response.meta['data_dir']
        
        if "title" in meta:
            item["title"] = meta["title"]
        if "author" in meta:
            item["author"] = meta["author"]
        if "publish_time" in meta:
            item["publish_time"] = meta["publish_time"]
        
        if response.url.find("ld_history_jianghua")!=-1:
            contents = Selector(text=response.body.decode("gbk")).xpath(self.xpath["content1"]).extract()
            #contents = Selector(text=response.body.decode("gbk")).xpath('//td[@class="dada"]/p').extract()
        else:
            contents = Selector(text=response.body.decode("gbk")).xpath(self.xpath["content2"]).extract()
            #contents = Selector(text=response.body.decode("gbk")).xpath('//td[@class="unnamed1"]/div[@align="left"]').extract()
            
        if len(contents)>0:
            
            content = contents[0]
            #print content
            content = self.body_prefix + content + self.body_suffix
            
            # md5每次都需要初始化
            m = hashlib.md5()
            m.update(response.url)
            filename = response.meta['data_dir']+m.hexdigest()+".html"
            
            with open(filename,'w') as f:
                f.write(content)
            
            item['content_type'] = 2
            item['content_path'] = filename
            
            #print content
        yield item
