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

    name = "cssn"
    
#     classify2url = getSiteEntryUrl(name)
#     xpath = getSiteXpath(name)
                    
    def getTotalPage(self,response):
        
        urls = [response.url,]
        m = re.search(r'countPage = (\d+)',response.body)
        
        if m:
            total_count = m.group(1)
            for i in range(1,int(total_count)):
                urls.append(response.url +"index_%s.shtml" % i)
        
        for url in urls:
            yield Request(url, callback=self.getArticleUrl, meta=response.meta,dont_filter=True)
                
    def getArticleUrl(self,response):
        
        meta=response.meta
        
        article_urls = response.xpath(self.xpath["article_link"]).extract()
        #article_urls = response.xpath('//div[@class="f-main-leftMain-content clear"]//ol/li/a/@href').extract()
        
        if len(article_urls) > 0:
            for url in article_urls:
                if url.startswith("./"):
                    url = response.meta['url_prefix'] + url.lstrip("./")
                
                if not url.startswith("http://"):
                    continue
                
                meta['url'] = url
                if isArticleExist(url) == False:
                    yield Request(url, callback=self.getContent, meta=meta, dont_filter=True)
    
    def getContent(self,response):
        
        #print response.body
        #sys.exit()
        meta = response.meta
                
        titles = response.xpath(self.xpath["title"]).extract()
        #titles = response.xpath('//span[@class="TitleFont"]/text()').extract()
        if len(titles) > 0:
            meta['title'] = titles[0]
            
        subdata = response.xpath(self.xpath["head"]).extract()
        #subdata = response.xpath('//div[@class="TitleFont2"]/text()').extract()
        if len(subdata)>0:
            m = re.search(u"(\d{4})年(\d{2})月(\d{2})",subdata[0])
            if m:
                day = '%s-%s-%s' % (m.group(1),m.group(2),m.group(3))
                meta['publish_time'] = day
            
            m = re.search(u"作者：(\S+)\s+",subdata[0])
            if m:
                author = m.group(1)
                meta['author'] = author
                
            m = re.search(u"来源：(\S+)\s+",subdata[0])
            if m:
                source = m.group(1)
                meta['source'] = source
                
        abstracts = ""
        abstracts_texts = response.xpath(self.xpath["abstract1"]).extract()
        #abstracts_texts = response.xpath(u'//span[@id="ChDivSummary"]/font/text()').extract() 
        for abstract in abstracts_texts:
            abstracts += abstract.strip()
        if len(abstracts_texts) == 0:
            abstracts_texts = response.xpath(self.xpath["abstract2"]).extract()
            #abstracts_texts = response.xpath(u'//div[@class="TRS_Editor"]//font/strong[contains(text(),"摘要") or contains(text(),"提要")]/../text()').extract() 
            for abstract in abstracts_texts:
                abstracts += abstract.strip()
        meta['abstract'] = abstracts
                
        keywords = ""
        keywords_texts = response.xpath(self.xpath["keyword1"]).extract()
        #keywords_texts = response.xpath(u'//span[@id="ChDivKeyWord"]/text()').extract() 
        for kwyword in keywords_texts:
            keywords += kwyword.strip()
        if len(keywords_texts) == 0:
            keywords_texts = response.xpath(self.xpath["keyword2"]).extract()
            #keywords_texts = response.xpath(u'//div[@class="TRS_Editor"]//font/strong[contains(text(),"键")]/../text()').extract() 
            for kwyword in keywords_texts:
                keywords += kwyword.strip()
        meta['keywords'] = keywords          
        
        #计算总共有多少页
        total_page = 1
        current_page = 1

        m = re.search(u"var countPage = (\d+)",response.body)
        if m:
            total_page = int(m.group(1))
        
        url_list = [response.url,]
        if total_page > 1:
            for page_num in range(1,total_page):
                index = response.url.rfind(".")
                next_page = response.url[0:index]+"_"+str(page_num)+response.url[index:]
                url_list.append(next_page)
        
        meta["url_list"] = url_list
        meta["total_page"] = total_page
        meta["current_page"] = current_page
        
        print meta["total_page"],meta["current_page"]
        
        #正文中的附件
        yield Request(response.url, callback=self.getEveryPage, meta=meta, dont_filter=True)
                
    def getEveryPage(self,response):
        meta = response.meta
        
        contents = response.xpath(self.xpath["content1"]).extract()
        #contents = response.xpath('//div[@class="TRS_Editor"]').extract()
        if len(contents) == 0:
            contents = response.xpath(self.xpath["content2"]).extract()
            #contents = response.xpath('//div[@id="Zoom"]').extract()
        
        if len(contents)>0:
            content = contents[0].encode("utf-8")
            
            if 'content' not in meta:
                meta['content'] = content
            else:
                meta['content'] += content
                
        #正文中的图片、附件,需要下载
        if "file_urls" not in meta:
            file_urls = []
        else:
            file_urls = meta["file_urls"]
            
        attachments = response.xpath(self.xpath["attachment"]).extract()
        #attachments = response.xpath('(//div[@class="TRS_Editor"]|//div[@id="Zoom"])[1]//img/@src | (//div[@class="TRS_Editor"]|//div[@id="Zoom"])[1]//a[contains(@href,"pdf")]/@href').extract()
        
        for file_url in attachments:
            #只需下载相对路径的图片，才能恢复；完整网址的路径也能恢复
            if not file_url.startswith("./"):
                continue
            else:
                index = response.url.rfind("/")
                if index != -1:
                    file_url = response.url[0:index]+file_url.lstrip(".")
                    file_urls.append(file_url)
                    
        meta['file_urls'] = file_urls
        
        if meta["current_page"] < meta["total_page"]:
            url = meta["url_list"][meta["current_page"]]
            print url
            meta["current_page"] += 1
            
            yield Request(url, callback=self.getEveryPage, meta=meta, dont_filter=True)
            
        else:
            
            item = ArticleItem()
            item['url'] = meta['url']
            item['classify'] = meta['classify']
            item['data_dir'] = meta['data_dir']
            item['title'] = meta['title']
            item['publish_time'] = meta['publish_time']
            if "author" in meta:
                item['author'] = meta['author']
            item['keywords'] = meta['keywords']
            item['abstract'] = meta['abstract']           
            item['file_urls'] = meta['file_urls']
            
            content = self.body_prefix + meta["content"] + self.body_suffix
            
            # md5每次都需要初始化
            m = hashlib.md5()
            m.update(response.url)
            filename = response.meta['data_dir']+m.hexdigest()+".html"
            with open(filename,'w') as f:
                f.write(content)
            item['content_path'] = filename
            
            item['content_type'] = 2
            
            yield item
            