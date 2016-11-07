# encoidng:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import os
import hashlib
from articles.settings import work_dir
from articles.utils import getSiteEntryUrl,getSiteXpath
import logging

class BaseSpider(CrawlSpider):
    
    body_prefix = "<html><head><meta charset='utf-8'></head><body>"
    body_suffix = "</body></html>"
     
    logger = logging.getLogger(__name__)
     
    def __init__(self, urlids=None, *a, **kw):

        #super(self.__class__, self).__init__(*a, **kw)
        
        self.data_dir = work_dir+self.name+"/"
        if not os.path.exists(self.data_dir): 
            os.makedirs(self.data_dir)
        
        print self.name,urlids
        self.classify2url = getSiteEntryUrl(self.name,urlids)
        
        self.logger.info("get urlids:{0} urls:\n{1}".format(urlids,"\n".join(self.classify2url.values())))
        
        self.xpath = getSiteXpath(self.name)
    
    def start_requests(self):

        for classify,url in self.classify2url.iteritems():

            if not sys.platform.startswith("win"):
                data_dir = self.data_dir + classify+"/"
            else:
                data_dir = self.data_dir + classify.encode("GBK")+"/"
            if not os.path.exists(data_dir): 
                os.makedirs(data_dir)
            
            meta = {"classify":classify,"url_prefix":url,"data_dir":data_dir}
            yield Request(url, callback=self.getTotalPage, meta=meta)
            
class MaterialSpider(CrawlSpider):
    
    def __init__(self, *a, **kw):

        #super(self.__class__, self).__init__(*a, **kw)
        self.data_dir = work_dir+self.name+"/"
        if not os.path.exists(self.data_dir): 
            os.makedirs(self.data_dir)
    