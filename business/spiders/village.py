# encoding: utf-8

from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log
from urllib import quote,unquote,urlencode

import sys
import simplejson
import re

reload(sys)
sys.setdefaultencoding("utf-8")

class AmazonSpider(CrawlSpider):

    name = "village"
    
    API = 'http://api.map.baidu.com/geoconv/v1/?'
    
    def start_requests(self):
        
        city2chinese = {"beijing":"北京市",
                        "shanghai":"上海市",
                        "guangzhou":"广州市",
                        "shenzhen":"深圳市",
                        "tianjin":"天津市",
                        }
        
        city2cityid = {"beijing":131,
                        "shanghai":289,
                        "guangzhou":257,
                        "shenzhen":340,
                        "tianjin":332,
                       }
        
        for city,chinese in city2chinese.iteritems():
            for business in open("area/%s_village.txt" % city).readlines():
                business = business.strip()
                business_name = chinese+business
                
                url = "http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%s" % business_name 
                url = url+"&c="+str(city2cityid[city])+"&src=0&wd2=&sug=0&l=15&from=webmap&biz_forward={%22scaler%22:1,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12967430.160684,4838625.341431&ie=utf-8"
                
                yield Request(url, callback=self.parse_uid,meta={"business":business,"cityid":city2cityid[city],"city":city})
    
    def parse_uid(self, response):
        
        meta = response.meta
        
        data = simplejson.loads(response.body)
        
        if data.get("content") is not None and len(data["content"]) > 0:
            
            area = None
            for i in range(len(data["content"])):
                if data["content"][i].get("std_tag") is not None and data["content"][i]["std_tag"] == "房地产;住宅区":
                    area = data["content"][i]
                    break
                
            if area is not None:
                uid = area["uid"]

                url = "http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=ext&uid=%s" % uid 
                url = url+"&c="+str(meta["cityid"])+"&ext_ver=new&tn=B_NORMAL_MAP&nn=0&u_loc=12967430.160684,4838625.341431&ie=utf-8&l=14&b=(12956715.25,4831097.35;12981067.25,4839193.35)&t=1460442626246"
                 
                yield Request(url, callback=self.parse_json,meta=meta)
                    
    def parse_json(self,response):
        
        data = simplejson.loads(response.body)
        
        if data.get('content') is not None and data['content'].get('geo') is not None:

            if len(data['content']['geo'])>0:
                geo = data['content']['geo'].split("|")[2]
                geo = geo.strip(";")[2:].split(",")
                geolist = []
                
                for i in range(0,len(geo)/2):
                    geolist.append(geo[2*i]+","+geo[2*i+1])
                    
                coords = ";".join(geolist)
                
                data = {"coords":coords,
                        "from":6,
                        "to:":5,
                        "ak":'uf77T9ZHeLvZgDkc5IGgPzoO'}
                
                url = self.API + urlencode(data)
                
                yield Request(url, callback=self.convertCoord, meta=response.meta)
                
    def convertCoord(self,response):
        data = simplejson.loads(response.body)
        
        if int(data['status']) == 0 :
            results = data['result']
            
            pos = response.meta["business"]+"\t"
            for result in results:
                pos = pos + str(result["x"])+","+str(result["y"])+";"
            
            fp = open("area/%s_village_area.txt" % response.meta["city"],"a")
             
            fp.write(pos+"\n")
        