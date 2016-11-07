# encoding: utf-8

import sys
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log

reload(sys)
sys.setdefaultencoding("utf-8")

class AmazonSpider(CrawlSpider):

    name = "anjuke"
    
    API = 'http://api.map.baidu.com/geoconv/v1/?'
    
    def start_requests(self):
        
        url = "http://www.anjuke.com/%s/cm/p%s/"
        
        city2page = {"beijing":115,
                       "shanghai":196,
                       "guangzhou":91,
                       "shenzhen":63,
                       "tianjin":61
                    }

        for city,pagecount in city2page.iteritems():
            for i in range(1,pagecount+1):
                requese_url = url % (city,i)
                yield Request(requese_url,callback=self.parse_list,meta={"city":city})
    
    def parse_list(self,response):
        
        meta = response.meta
        fp = open("%s_village.txt" % meta["city"],"a")
        vliiages = response.xpath('//div[@id="content"]/ul[@class="P3"][1]/li/em/a/text()').extract()
        for village in vliiages:
            fp.write(village+"\n")