# encoding: utf-8

from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

import simplejson
import urllib
import random

class AmazonSpider(CrawlSpider):
    '''抓取指定矩形区域的关键点数据'''
    
    name = "keypoint"
    
    API = 'http://api.map.baidu.com/place/v2/search?'
    cityids = {
#               1:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#               2:'门$公交$路口$-1口$-2口$-3口$-4口$-5口$-6口$-7口$-8口$-9口$-10口$-11口$-12口$-13口$-14口$-15口$-16口',
#             3:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             4:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             15:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             16:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             17:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             18:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             19:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             37:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             38:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             40:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             41:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
            42:'门$公交$路口$-1口$-2口$-3口$-4口$-5口$-6口$-7口$-8口$-9口$-10口$-11口$-12口$-13口$-14口$-15口$-16口',
#             46:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             50:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             51:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             52:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             53:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             54:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             55:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             60:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             61:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             62:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             63:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             65:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             67:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             97:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             112:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             129:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             146:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             167:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             236:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             265:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             266:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             267:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             322:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             333:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             339:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             365:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口',
#             1315:'门$公交站$路口$-A口$-B口$-C口$-D口$-E口$-F口$-G口$-H口'
              }
    
    def __init__(self, *a, **kw):

        super(self.__class__, self).__init__(*a, **kw)
        
        self.aks = ['61oEbKGqEBkE5jN2xXx3CiZI',#我
                    #'uf77T9ZHeLvZgDkc5IGgPzoO',#子健
                    'mHG6eTMkxTsNBrwTgUtAqvKf',#孙博文
                    'qrrrbv0aCsIj6AlaUVXUtI34',#杜辉
                    #'eUR5ah6MQ5y3Sg6ST0penkoX',
                    'dmtP3rufYrXvFwBxxkkMW1Y9',#玉石
                    '5ru0ndvN4MCvykmtZOIlAZaf'#三虎
                    ]

    def start_requests(self):
        
        for cityid,querywords in self.cityids.iteritems():
            
            city_border_points = open('city_border/parts_%s.txt' % cityid).readlines()
            #city_border_points = open('city_border/parts.txt').readlines()
            
            for line in city_border_points:
                bounds = line.strip()  
                    
                meta = {
                'query':querywords,
                'bounds':bounds,
                'page_num':0,
                'page_size':20,
                'output':'json',
                'ak':random.choice(self.aks),
                'cityid':cityid
                }
                
                parmeters = urllib.urlencode(meta)
                
                url = self.API + parmeters
        
                yield Request(url, callback=self.parse_routine, meta=meta)
    
    def parse_routine(self, response):
        
        meta = response.meta
        
        data = simplejson.loads(response.body)
        
        fp = open('keypoints/point_%s.txt' % meta['cityid'],'a')
        
        for element in data['results']:
            location = element['location']
            uid = element['uid']
            name = element['name']
            address = element.get("address")
            telephone = element.get("telephone")
            
            result = '%s\t%.6f\t%.6f\t%s\t%s\t%s' % (
                                     uid,
                                     location['lng'],
                                     location['lat'],
                                     name,
                                     address,
                                     telephone)

            #print result
            fp.write(result.encode("utf-8")+'\n')
            
        if data['total'] > meta['page_size'] * (meta['page_num']+1):
            
            #更新字段
            meta['page_num'] += 1
            meta['ak'] = random.choice(self.aks)
            
            parmeters = urllib.urlencode(meta)
            
            url = self.API + parmeters
    
            yield Request(url, callback=self.parse_routine, meta=meta)
            