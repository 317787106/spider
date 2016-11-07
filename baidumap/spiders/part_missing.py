# encoding: utf-8

from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

import simplejson
import math
import urllib
import bisect
import random

class AmazonSpider(CrawlSpider):
    '''大城市拆分计算路口间距离'''
    
    name = "part_missing"
    
    API = 'http://api.map.baidu.com/direction/v1/routematrix?'
    
            
    def __init__(self, *a, **kw):

        super(self.__class__, self).__init__(*a, **kw)
    
    def getPair(self):
        
        pid2pidset = dict()
        with open("city_map/all_map_37_part1.txt") as f:
            for line in f:
                items = line.strip().split("\t")
                pid1 = int(items[0])
                pid2 = int(items[1])
                if pid1 not in pid2pidset:
                    pid2pidset[pid1] = set([pid2,])
                else:
                    pid2pidset[pid1].add(pid2)
        
        return pid2pidset
    
    def start_requests(self):
        pid2pidset = self.getPair()
        
        #上半部分
        city_border_points = open('city_map/all_map_371.txt').readlines()
        
        points = []
        for line in city_border_points:
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
            
        #下半部分
        city_border_points2 = open('city_map/all_map_372.txt').readlines()
        
        points2 = []
        for line in city_border_points2:
            items = line.strip().split()
            pointid = int(items[0])
            lon = float(items[1])
            lat = float(items[2])
            
            point = (pointid,lon,lat)
            points2.append(point)
        
        groups2 = []
        group_size2 = len(points2)/5
        if len(points2) % 5 > 0 :
            group_size2 += 1
            
        for i in range(group_size2):
            groups2.append(points2[i*5:(i+1)*5])
        
        #每次发送5*5的线路请求
        for i in range(group_size):
            group_start = groups[i]
            
            for j in range(group_size2):
                group_end = groups2[j]
                
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
                
                #判断是否应该发起请求
                exist = False
                for pid1 in start_point_ids:
                    for pid2 in end_point_ids:
                        if pid1 in pid2pidset and pid2 in pid2pidset[pid1]:
                            exist = True
                
                if exist == True:
                    continue
                
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
        
        fp = open('city_map/all_map_37_part1_1.txt','a')
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
            
            #print result
            fp.write(result)