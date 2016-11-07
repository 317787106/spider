# encoding: utf-8

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
import urllib

class AmazonSpider(BaseSpider):

    name = "mohrss"
    
    url_prefix = "http://www.mohrss.gov.cn/gkml/"
    
#     classify2url = getSiteEntryUrl(name)
#     xpath = getSiteXpath(name)
                    
    def getTotalPage(self,response):
        
        urls = []
        
        urls.append(response.url)
        if response.url.find("gkml") != -1:
            
            root_urls = response.xpath('//div[@isroot="true"]/a/@href').extract()
            if len(root_urls)>0:
                
                content = urllib.urlopen(self.url_prefix + root_urls[0].strip('./')).read()
                
                m1 = re.search(r'm_nRecordCount = \"(\d+)\";',content)
                m2 = re.search(r'm_nPageSize = (\d+);',content)
        
                if m1:
                    total_count = m1.group(1)
                if m2:
                    page_size = m2.group(1)
                    
                if total_count is not None and page_size is not None:
                    
                    total_page = int(total_count)/int(page_size)
        
                    for i in range(1,total_page):
                        url = "http://www.mohrss.gov.cn/gkml/81/83/list_%s.htm" % i
                        urls.append(url)
        else:
            m = re.search(r'var countPage = (\d+)',response.body)
            if m:
                total_count = m.group(1)
                for i in range(1,int(total_count)):
                    url = response.url +"index_%s.htm" % i
                    urls.append(url)
                      
        for url in urls:
            yield Request(url, callback=self.getArticleUrl, meta=response.meta,dont_filter=True)
                
    def getArticleUrl(self,response):
        
        meta = response.meta
        
        if response.url.find("gkml") != -1:
            
            article_urls = response.xpath(self.xpath["article_link_GKML"]).extract()
            #article_urls = response.xpath('//div[@id="documentContainer"]/div[@class="row"]/li[@class="mc"]//a/@href').extract()
            
            if len(article_urls) > 0:
                for url in article_urls:
                #for url in article_urls:
                    if url.startswith("../../"):
                        url = self.url_prefix + url.lstrip("../../")
                    
                    if not url.startswith("http://"):
                        continue
                    
                    meta['url'] = url
                    if isArticleExist(url) == False:
                        yield Request(url, callback=self.getContentGKML, meta=meta)
        else:
            article_urls = response.xpath(self.xpath["article_link_SYrlzyhshbzb"]).extract()
            #article_urls = response.xpath('//div[@class="serviceMainListConType"]/div/div[@class="serviceMainListTxt"]/span/a/@href').extract()
            
            if len(article_urls) > 0:
                for url in article_urls:
                    
                    index = response.url.rfind("/")
                    if url.startswith("./"):
                        url = response.url[0:index] + url.lstrip(".")
                    
                    if not url.startswith("http://"):
                        continue
                    
                    meta['url'] = url
                    if isArticleExist(url) == False:
                        yield Request(url, callback=self.getContentSYrlzyhshbzb, meta=meta)
    
    def getContentSYrlzyhshbzb(self,response):
        
        item = ArticleItem()
        item['url'] = response.meta['url']
        item['classify'] = response.meta['classify']
        item['data_dir'] = response.meta['data_dir']
        
        # md5每次都需要初始化
        m = hashlib.md5()
        m.update(response.url)
        md5name = m.hexdigest()
        
        titles = response.xpath(self.xpath["title_SYrlzyhshbzb"]).extract()
        #titles = response.xpath(u'//div[@class="insMainConTitle_b"]/font/text()|//div[@class="insMainConTitle_b"]/text()').extract()
        if len(titles) > 0:
            item['title'] = titles[0].strip()
            
        subdata = response.xpath(self.xpath["publish_time_SYrlzyhshbzb"]).extract()
        #subdata = response.xpath(u'//div[@class="insMainCon_b"]/div[@class="insMainConTitle_a"]/div[@class="insMainConTitle_c"]/text()').extract()
        if len(subdata)>0:
            m = re.search(u"(\d{4})-(\d{2})-(\d{2})",subdata[0])
            if m:
                day = '%s-%s-%s' % (m.group(1),m.group(2),m.group(3))
                item['publish_time'] = day                
                
        #正文中的图片、pdf附件、xml附件,需要下载
        file_urls = []
        urls = response.xpath(self.xpath["attachment_SYrlzyhshbzb"]).extract()     
        #urls = response.xpath(u'//div[@id="insMainConTxt"]//img/@src | //a[contains(@href,"pdf")]/@href | //a[contains(@href,"xls")]/@href').extract()
        
        #记录非图片格式的附件名字
        attachments_names = []
        for file_url in urls:
            print response.url,md5name,file_url
            #只需下载相对路径的图片，才能恢复；完整网址的路径也能恢复
            if file_url.startswith("./"):
                index = response.url.rfind("/")
                if index != -1:
                    file_url = response.url[0:index]+file_url.lstrip(".").strip()
                        
                    file_urls.append(file_url)
                    
            elif file_url.startswith("/"):
                file_url = "http://www.mohrss.gov.cn"+file_url.strip()
            
                file_urls.append(file_url)
        
            if file_url.endswith("pdf") or file_url.endswith("xls"):
                attachments_name = file_url.split('/')[-1]
                attachments_names.append(attachments_name)
        
        item['file_urls'] = file_urls
        
        contents = response.xpath(self.xpath["content_SYrlzyhshbzb"]).extract()
        #contents = response.xpath('//div[@id="insMainConTxt"]').extract()
        if len(contents) > 0:
            
            content = contents[0].encode("utf-8")
            
            #附件链接添加到文章结尾
            for attachments_name in attachments_names:
                content = content + "<a target=\"_blank\" href=\"./%s\">附件-%s</a>" % (attachments_name,attachments_name)
                
            content = self.body_prefix + content + self.body_suffix
            
            filename = response.meta['data_dir']+md5name+".html"
            
            with open(filename,'w') as f:
                f.write(content)
            
            item['content_type'] = 2 
            item['content_path'] = filename
        
        #正文中的附件
        yield item
    
            
    def getContentGKML(self,response):
        
        item = ArticleItem()
        item['url'] = response.meta['url']
        item['classify'] = response.meta['classify']
        item['data_dir'] = response.meta['data_dir']
        
        titles = response.xpath(self.xpath["title_GKML"]).extract()
        #titles = response.xpath('//div[@class="govInfoMainCon"]/div[@class="govInfoMainTabListTxtTab"]/text()').extract()
        if len(titles) > 0:
            item['title'] = titles[0].strip()
            
        subdata = response.xpath(self.xpath["publish_time_GKML"]).extract()
        #subdata = response.xpath('(//div[@class="govInfoMainTab"]/div[@class="govInfoMainTabList"][2]/div[@class="govInfoMainTabList_a"]\
        #    /div[@class="govInfoMainTabListTxt"])[2]/text()').extract()
        if len(subdata)>0:
            m = re.search(u"(\d{4})年(\d{2})月(\d{2})",subdata[0])
            if m:
                day = '%s-%s-%s' % (m.group(1),m.group(2),m.group(3))
                item['publish_time'] = day
            
        subdata = response.xpath(self.xpath["author_GKML"]).extract()
        #subdata = response.xpath('(//div[@class="govInfoMainTab"]/div[@class="govInfoMainTabList"][2]/div[@class="govInfoMainTabList_a"]\
        #    /div[@class="govInfoMainTabListTxt"])[1]/text()').extract()
        if len(subdata) >= 2:
            item['author'] = subdata[1].strip()
                
        contents = response.xpath(self.xpath["content_GKML"]).extract()
        #contents = response.xpath('//div[@class="govInfoMainTabListTxtMain"]').extract()
        if len(contents)>0:
            
            content = contents[0].encode("utf-8")
            content = self.body_prefix + content + self.body_suffix
            
            m = hashlib.md5()
            m.update(response.url)
            filename = response.meta['data_dir']+m.hexdigest()+".html"
            
            with open(filename,'w') as f:
                f.write(content)
            
            item['content_type'] = 2 
            item['content_path'] = filename
                
        #正文中的图片、附件,需要下载
        file_urls = []
        urls = response.xpath(self.xpath["attachment_GKML"]).extract()
        #urls = response.xpath('//div[@class="govInfoMainTabListTxtMain"]//img/@src').extract()
        
        for file_url in urls:
            #只需下载相对路径的图片，才能恢复；完整网址的路径也能恢复
            if not file_url.startswith("./"):
                continue
            else:
                index = response.url.rfind("/")
                if index != -1:
                    file_url = response.url[0:index]+file_url.lstrip(".")
            
                    file_urls.append(file_url)
            
        item['file_urls'] = file_urls
        
        #正文中的附件
        yield item