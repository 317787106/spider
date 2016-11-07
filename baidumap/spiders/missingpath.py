# encoding: utf-8

from scrapy.spiders import CrawlSpider
from scrapy.http import Request

import simplejson
import math
import urllib
import bisect
import random

from baidumap.distance import getDistanceByTwoPosition

class AmazonSpider(CrawlSpider):
    '''计算增量路径的长度'''
    
    name = "missingpath"
    
    API = 'http://api.map.baidu.com/direction/v1/routematrix?'
    #1,2,3,4,15,16,17,18,19,37,38,40,41,42,46,50,51,52,53,54,55,60,61,62,63,65,67,97,112,129,146,167,236,265,266,267,322,333,339,365,1315
    cityid = 2
    
    def __init__(self, *a, **kw):

        super(self.__class__, self).__init__(*a, **kw)
        
        self.fp = open('missing_path_%s_result.txt' % self.cityid,'w')

    def start_requests(self):
    
        pid2pos = self.getPid2Pos()
        lines = open('missing_path_%s.txt' % self.cityid).readlines()
        
        for line in lines:
            items = line.strip().split("\t")
            src_pid = int(items[0])

            long1 = pid2pos[src_pid][0]
            lati1 = pid2pos[src_pid][1]
            
            dst_length = len(items)-1
            max_array_length = dst_length/5
            if dst_length % 5 > 0 :
                max_array_length += 1
            
            for i in range(max_array_length):
                pids = [int(item) for item in items[(5*i+1):(5*(i+1)+1)]]
                destinations = []
                pointids = []
                
                for dst_pid in pids:
                    long2 = pid2pos[dst_pid][0]
                    lati2 = pid2pos[dst_pid][1]
                    
                    destinations.append("%s,%s"%(lati2,long2))
                    pointids.append(dst_pid)
                        
                if len(destinations) == 0:
                    continue        
                
                destinations = "|".join(destinations)
                
                parameter = {
                'mode':'driving',
                'origins':'%s,%s' % (lati1,long1),
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
                        'src_pid':src_pid,
                        'end_point_ids':pointids,
                        }
                
                url = self.API + parmeters

                yield Request(url, callback=self.parse_routine, meta=meta)
    
    def parse_routine(self, response):
        
        meta = response.meta
        
        data = simplejson.loads(response.body)
        
        index = 0
        for element in data['result']['elements']:
            distance = element['distance']['value']
            
            if int(distance) == 0:
                distance = 99999999
            result = '%s\t%s\t%s' % (
                                     meta['src_pid'],
                                     meta['end_point_ids'][index],
                                     distance)
            index += 1
            #print result
            self.fp.write(result+'\n')
            
    def getPid2Pos(self):
        lines = open('city_map/all_map_%s.txt' % self.cityid).readlines()
        pid2pos = dict()
        for line in lines:
            pid = int(line.strip().split("\t")[0])
            longtitude = float(line.strip().split("\t")[1])
            latitude = float(line.strip().split("\t")[2])
            pid2pos[pid] = (longtitude,latitude)
            
        return pid2pos