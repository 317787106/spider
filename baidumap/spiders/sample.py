# encoding: utf-8

from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

import simplejson
import urllib
import random


class AmazonSpider(CrawlSpider):
    '''计算数据库中已有跨城订单的百度距离'''
    
    name = "sample"
    
    API = 'http://api.map.baidu.com/direction/v1/routematrix?'
            
    def __init__(self, *a, **kw):

        super(self.__class__, self).__init__(*a, **kw)
        
        self.fp = open('sample/sample_ride_after.txt','w')
        
    def start_requests(self):
    
        lines = open('sample/sample_ride.txt').readlines()
        
        for line in lines:
            items = line.strip().split("\t")
            rideid = items[0]
            cityid = items[1]
            long1 = items[2]
            lati1 = items[3]
            long2 = items[4]
            lati2 = items[5]
            onlinedistance = items[6]
            
            parameter = {
            'mode':'driving',
            'origins':'%s,%s' % (lati1,long1),
            'destinations':'%s,%s' % (lati2,long2),
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
            
            meta = {
                    'rideid':rideid,
                    'cityid':cityid,
                    'long1':long1,
                    'lati1':lati1,
                    'long2':long2,
                    'lati2':lati2,
                    'onlinedistance':onlinedistance
                    }
            
            url = self.API + parmeters

            yield Request(url, callback=self.parse_routine, meta=meta)
    
    def parse_routine(self, response):
        
        meta = response.meta
        
        data = simplejson.loads(response.body)
        
        for element in data['result']['elements']:
            distance = element['distance']['value']
            result = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
                                     meta['rideid'],
                                     meta['cityid'],        
                                     meta['long1'],
                                     meta['lati1'],
                                     meta['long2'],
                                     meta['lati2'],
                                     meta['onlinedistance'],
                                     distance)

            self.fp.write(result+'\n')
            