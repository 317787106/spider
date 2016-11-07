# encoding: utf-8

from __future__ import division

from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

import simplejson
import urllib
import random

class AmazonSpider(CrawlSpider):

    name = "address"
    
    API = 'http://api.map.baidu.com/geocoder/v2/?'
    
    def start_requests(self):
        lines = open("street/points3_address.txt").readlines()
        ids = set([ int(line.strip().split("\t")[0]) for line in lines])
        
        with open("street/points3.txt") as f:
            
            for line in f:
                items = line.strip().split("\t")
            
                pid = int(items[0])
                lon = float(items[1])
                lat = float(items[2])
                
                if pid in ids:
                    continue
                
                meta = {
                    'output' : 'json',
                    'ak':random.choice(['61oEbKGqEBkE5jN2xXx3CiZI',#我
                                        #'rtTROFg2VMSIGdDKcYfc8fKWtMSDui3B',#丙贤
                                        'mHG6eTMkxTsNBrwTgUtAqvKf',#孙博文
                                        'qrrrbv0aCsIj6AlaUVXUtI34',#杜辉
                                        #'Z6ku8SEzr6ZVRNaxpU1k0ogVeAKlxcGO',#丹丹
                                        'dmtP3rufYrXvFwBxxkkMW1Y9',#玉石
                                        '5ru0ndvN4MCvykmtZOIlAZaf'#三虎
                                        ]),
                    'location':'%s,%s' % (lat,lon),
                    'pois':0
                }
                
                parmeters = urllib.urlencode(meta)
                
                url = self.API + parmeters
                
                meta['pid'] = pid
                meta['lon'] = lon
                meta['lat'] = lat

                yield Request(url, callback=self.parse_list, meta=meta)
                
    
    def parse_list(self, response):
        
        meta = response.meta

        data = simplejson.loads(response.body)
        
        if data['status'] == 0:
            
            fp = open("street/points3_address.txt","a")
            addressComponent = data['result']['addressComponent']
            
            fp.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\n".format(
                meta['pid'],
                meta['lon'],
                meta['lat'],
                addressComponent['province'].encode("utf-8"),
                addressComponent['city'].encode("utf-8"),
                addressComponent['district'].encode("utf-8"),
                addressComponent['street'].encode("utf-8"),
                addressComponent['street_number'].encode("utf-8"),
                data['result']['business'].encode("utf-8")))
            
            fp.close()
        else:
            print response.url,data