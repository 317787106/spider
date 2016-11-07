# encoding: utf-8

from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

import simplejson
import math
import urllib
import bisect
import random

class AmazonSpider(CrawlSpider):
    '''计算城市间任意2个路口的距离'''
    
    name = "anycity"
    
    API = 'http://api.map.baidu.com/direction/v1/routematrix?'
    cityid = 202
    
    def __init__(self, *a, **kw):

        super(self.__class__, self).__init__(*a, **kw)

    def start_requests(self):
        
        city_cross_points = open('city_map/all_map_%s.txt' % self.cityid).readlines()
        
        self.fp = open('city_map/all_map_%s_p2p.txt' % self.cityid,'w')
        
        points = []
        for line in city_cross_points:
            items = line.strip().split()
            pointid = int(items[0])
            lon = float(items[1])
            lat = float(items[2])
            
            point = (pointid,lon,lat)
            points.append(point)
            
        groups = []
        group_size = len(points)/5
        if len(points) % 5 > 0 :
            group_size += 1
            
        for i in range(group_size):
            groups.append(points[i*5:(i+1)*5])
        
        #每次发送5*5的线路请求
        for i in range(group_size):
            group_start = groups[i]
            
            for j in range(group_size):
                group_end = groups[j]
                
#                 #单向路线
#                 if i>j:
#                     continue
                
                start_point_ids = []
                origins = []
                for point in group_start:
                    start_point_ids.append(point[0])
                    origins.append("%s,%s"%(point[2],point[1]))
                
                end_point_ids = []
                destinations = []
                for point in group_end:
                    end_point_ids.append(point[0])
                    destinations.append("%s,%s"%(point[2],point[1]))
                
                origins = "|".join(origins)              
                destinations = "|".join(destinations)
                
                parameter = {
                'mode':'driving',
                'origins':origins,
                'destinations':destinations,
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
                        'start_point_ids':start_point_ids,
                        'end_point_ids':end_point_ids,
                        }
                
                url = self.API + parmeters
                
                yield Request(url, callback=self.parse_routine, meta=meta)
    
    def parse_routine(self, response):
        
        meta = response.meta
        
        data = simplejson.loads(response.body)
        
        index = 0

        end_points_size = len(meta['end_point_ids'])
        
        for element in data['result']['elements']:
            distance = element['distance']['value']
            
            start_point_id = meta['start_point_ids'][index / end_points_size]
            end_point_id = meta['end_point_ids'][index % end_points_size]
            
            index += 1
            
            if start_point_id == end_point_id:
                continue
            
            if int(distance) == 0:
                distance = 99999999
            result = '%s\t%s\t%s\n' % (start_point_id, end_point_id, distance)
            
            self.fp.write(result)