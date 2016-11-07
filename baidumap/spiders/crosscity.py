# encoding: utf-8

from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

import simplejson
import math
import urllib
import bisect
import random

from baidumap.distance import getDistanceByTwoPosition

class AmazonSpider(CrawlSpider):
    '''计算城市间2个高速口的距离'''
    
    name = "crosscity"
    
    API = 'http://api.map.baidu.com/direction/v1/routematrix?'
    cityids = [
            1,
            ]
            
    def __init__(self, *a, **kw):

        super(self.__class__, self).__init__(*a, **kw)

    def start_requests(self):
        
        
        city_border_points = open('city_border_points.txt').readlines()
        
        max_array_length = len(city_border_points)/5
        if len(city_border_points)%5 > 0 :
            max_array_length += 1
        
        for j in range(len(city_border_points)):
            city_border_point1 = city_border_points[j]
            pointid1 = city_border_point1.strip().split()[0]
            cityid1 = int(pointid1.split('_')[0])
            long1 = float(city_border_point1.strip().split()[1])
            lati1 = float(city_border_point1.strip().split()[2])
            
            for i in range(max_array_length):
                arrays = city_border_points[5*i:5*(i+1)]
                destinations = []
                pointids = []
                
                for array in arrays:
                    pointid2 = array.strip().split()[0]
                    cityid2 = int(pointid2.split('_')[0])
                    long2 = array.strip().split()[1]
                    lati2 = array.strip().split()[2]
                    
                    if cityid1 >= cityid2:
                        continue
                    else:
                        destinations.append("%s,%s"%(lati2,long2))
                        pointids.append(pointid2)
                        
                if len(destinations) == 0:
                    continue        
                
                destinations = "|".join(destinations)
                
                parameter = {
                'mode':'driving',
                'origins':'%s,%s' % (lati1,long1),
                'destinations':destinations,
                'output':'json',
                'ak':random.choice(['61oEbKGqEBkE5jN2xXx3CiZI',
                                    'uf77T9ZHeLvZgDkc5IGgPzoO',
                                    'mHG6eTMkxTsNBrwTgUtAqvKf',
                                    'qrrrbv0aCsIj6AlaUVXUtI34',
                                    'eUR5ah6MQ5y3Sg6ST0penkoX',
                                    'dmtP3rufYrXvFwBxxkkMW1Y9',
                                    '5ru0ndvN4MCvykmtZOIlAZaf']),
                }
                
                parmeters = urllib.urlencode(parameter)
                
                meta = {
                        'start_city_pointid':pointid1,
                        'end_point_ids':pointids,
                        }
                
                url = self.API + parmeters

                yield Request(url, callback=self.parse_routine, meta=meta)
    
    def parse_routine(self, response):
        
        meta = response.meta
        
        data = simplejson.loads(response.body)
        
        fp = open('city_border_path_distance.txt','a')
        
        index = 0
        for element in data['result']['elements']:
            distance = element['distance']['value']
            result = '%s\t%s\t%s' % (
                                     meta['start_city_pointid'],
                                     meta['end_point_ids'][index],
                                     distance)
            index += 1
            print result
            fp.write(result+'\n')
            