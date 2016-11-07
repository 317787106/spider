# encoding: utf-8

from __future__ import division

from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

import simplejson
import math
import urllib

class AmazonSpider(CrawlSpider):

    name = "baidu"
    
    API = 'http://api.map.baidu.com/place/v2/search?'

            
    def __init__(self, *a, **kw):

        super(self.__class__, self).__init__(*a, **kw)
        self.city2square = dict() 
        
        self.cityids = [
            int(line.strip().split('\t')[0]) for line in open('unservice_city_square.txt').readlines()
            ]
        
        for line in open('unservice_city_square.txt').readlines():
            items = line.strip().split()
            city_id = int(items[0])
            LT_lon = float(items[1])
            LT_lat = float(items[2])
            RD_lon = float(items[3])
            RD_lat = float(items[4])
            cityname = items[5]
            self.city2square[city_id] = (LT_lon,LT_lat,RD_lon,RD_lat,cityname)
    
    def start_requests(self):
        
        #self.log('total products: %s' % len(self.start_urls), level=log.INFO)
        
        for cityid in self.cityids:
            
            interval = 0.05
            square = self.city2square[cityid]
            
            step_lon = int((square[2] - square[0])/interval)
            step_lat = int((square[3] - square[1])/interval)
            cityname = square[4]
            
            print step_lon,step_lat
            for i in range(0,step_lon):
                for j in range(0,step_lat,-1):
                    LT_lon = square[0]+interval*i
                    LT_lat = square[1]+interval*j
                    RD_lon = square[0]+interval*(i+1)
                    RD_lat = square[1]+interval*(j+1)
                    
                    meta = {
                    'query' : '路口', 
                    'region' : cityname, 
                    'bounds' : '{0},{1},{2},{3}'.format(LT_lat,LT_lon,RD_lat,RD_lon),
                    'output' : 'json',
                    'ak' : 'mHG6eTMkxTsNBrwTgUtAqvKf',
                    'scope' : 2,
                    'page_size' :20,
                    'page_num' : 0
                    }
                    parmeters = urllib.urlencode(meta)
                    
                    meta['cityid'] = cityid
                    
                    url = self.API + parmeters
    
                    yield Request(url, callback=self.parse_list, meta=meta)
    
    def parse_list(self, response):
        
        meta = response.meta
        data = simplejson.loads(response.body)
        
        total = data['total']
        current_page = meta['page_num']
        
        #空白
        if total == 0:
            return 
        
        print response.url
        fp = open('/home/jiangyuanshu/baidumap_data/%s/%s_%s_%s.json' % (meta['cityid'],meta['bounds'].split(',')[0],meta['bounds'].split(',')[1],current_page),'w')
        fp.write(response.body)
        fp.close() 
        
        #抓取后续页面
        if current_page < int(math.ceil(total/20))-1:
            meta['page_num'] += 1
            #先删掉cityid，编码完成后再加上
            cityid = meta['cityid']
            del meta['cityid']
            parmeters = urllib.urlencode(meta)
            url = self.API + parmeters
            meta['cityid'] = cityid
            yield Request(url, callback=self.parse_list, meta=meta)
        else:
            return
        