# encoding: utf-8

import sys
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

import random
import urllib
import simplejson

reload(sys)
sys.setdefaultencoding("utf-8")

class AmazonSpider(CrawlSpider):

    name = "point2business"
    
    API = 'http://api.map.baidu.com/geocoder/v2/?'
    
    def start_requests(self):
        
        citys = ["beijing",
                "shanghai",
                "guangzhou",
                "shenzhen",
                "tianjin"
                ]

        for city in citys:
            for line in open("area/%s_map_point.txt" % city):
                items = line.strip().split()
                
                parameter = {
                    'location':'%s,%s'%(items[1],items[0]),
                    'pois':0,
                    'output':'json',
                    'ak':random.choice(['61oEbKGqEBkE5jN2xXx3CiZI',#我
                                        #'uf77T9ZHeLvZgDkc5IGgPzoO',#子健
                                        'mHG6eTMkxTsNBrwTgUtAqvKf',#孙博文
                                        'qrrrbv0aCsIj6AlaUVXUtI34',#杜辉
                                        #'eUR5ah6MQ5y3Sg6ST0penkoX',
                                        'dmtP3rufYrXvFwBxxkkMW1Y9',#玉石
                                        '5ru0ndvN4MCvykmtZOIlAZaf'#三虎
                                        ]),
                }
                
                parmeters = urllib.urlencode(parameter)
                
                url = self.API + parmeters

                yield Request(url, callback=self.parse_business, meta={"city":city})
    
    def parse_business(self,response):
        
        meta = response.meta
        
        data = simplejson.loads(response.body)
        if data["status"] != 0:
            return
        
        business = data["result"]["business"]
        
        fp = open("area/%s_business.txt" % meta["city"],"a")
        for item in business.split(","):
            if len(item) > 0:
                fp.write(item+"\n")
