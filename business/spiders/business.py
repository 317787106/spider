# encoding: utf-8

from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request,FormRequest
from scrapy import log
from urllib import quote,unquote,urlencode

import sys
import simplejson
import re

reload(sys)
sys.setdefaultencoding("utf-8")

class AmazonSpider(CrawlSpider):

    name = "business"
    
    API = 'http://api.map.baidu.com/geoconv/v1/?'
    
    def start_requests(self):
        
        city2chinese = {"beijing":"北京市",
                        #"shanghai":"上海市",
                        #"guangzhou":"广州市",
                        #"shenzhen":"深圳市",
                        #"tianjin":"天津市",
                        }
        
        city2cityid = {"beijing":131,
                        "shanghai":289,
                        "guangzhou":257,
                        "shenzhen":340,
                        "tianjin":332,
                       }
        
        for city,chinese in city2chinese.iteritems():
            for business in open("area/%s_business.txt" % city).readlines():
                business = business.strip()
                business_name = quote(chinese+business)
                
                url = "http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%s" % business_name 
                url = url+"&c="+str(city2cityid[city])+"&src=0&wd2=&sug=0&l=15&from=webmap&biz_forward={%22scaler%22:1,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12967430.160684,4838625.341431&ie=utf-8"
                
                cookies = {"BAIDUID":"AEB2444D952F178103892DAF57ECCDF0:FG=1",
                           "BIDUPSID":"AEB2444D952F178103892DAF57ECCDF0",
                           "PSTM":"1451796604",
                           "MCITY":"-131%3A"
                           }
                
                #print url
                yield Request(url, callback=self.parse_uid,cookies=cookies,meta={"business":business,"cityid":city2cityid[city],"city":city})
    
    def parse_uid(self, response):
        
        meta = response.meta

        data = simplejson.loads(response.body)
        
        #print response.body
        if data.get("content") is not None and len(data["content"]) > 0:
            for i in range(len(data["content"])):

                area = data["content"][i]
                if area.get("std_tag") is None or area["std_tag"].find("住宅区")!=-1 or area["std_tag"].find("医院")!=-1 \
                or area["std_tag"].find("房地产")!=-1 or area["std_tag"].find("酒店")!=-1:
                    continue
                
                uid = area["uid"]
                meta["business"] = area["name"]
                
                url = "http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=ext&uid=%s" % uid 
                url = url+"&c="+str(meta["cityid"])+"&ext_ver=new&tn=B_NORMAL_MAP&nn=0&u_loc=12967430.160684,4838625.341431&ie=utf-8&l=14&b=(12956715.25,4831097.35;12981067.25,4839193.35)&t=1460442626246"
                 
                #print url
                yield Request(url, callback=self.parse_json,meta=meta)
                    
    def parse_json(self,response):
        
        data = simplejson.loads(response.body)
        meta = response.meta
        if data.get('content') is not None and data['content'].get('geo') is not None:

            if len(data['content']['geo'])>0:
                geo = data['content']['geo'].split("|")[2]
                geo = geo.strip(";")[2:].split(",")
                geolist = []
                
                for i in range(0,len(geo)/2):
                    geolist.append(geo[2*i]+","+geo[2*i+1])
                
                #API限制geolist长度不能超过100
                if len(geolist)>100:
                    coords = ";".join(geolist[0:100])
                    #下次再请求
                    meta['left_coords'] = ";".join(geolist[100:])
                else:
                    coords = ";".join(geolist)
                    
                data = {"coords":coords,
                        "from":str(6),
                        "to":str(5),
                        "ak":'uf77T9ZHeLvZgDkc5IGgPzoO'}
                
                yield FormRequest(self.API, callback=self.convertCoord, method="POST", formdata=data,meta=meta,dont_filter=True)
                
    def convertCoord(self,response):
        
        data = simplejson.loads(response.body)
        meta = response.meta
        
        print meta
        if int(data['status']) == 0 :
            results = data['result']
            
            pos = ""
            for result in results:
                pos = pos + str(result["x"])+","+str(result["y"])+";"
            
            if meta.get("left_coords") is not None:
                data = {"coords":response.meta.get("left_coords"),
                        "from":str(6),
                        "to":str(5),
                        "ak":'uf77T9ZHeLvZgDkc5IGgPzoO'}
                
                del meta["left_coords"]
                
                meta["pos"] = pos
                yield FormRequest(self.API, callback=self.convertCoord, method="POST", formdata=data,meta=response.meta,dont_filter=True)
            else:    
                if meta.get("pos") is not None:
                    pos = response.meta["business"]+"\t" + meta.get("pos") + pos
                else:
                    pos = response.meta["business"]+"\t" + pos
                    
                print pos
                
                fp = open("area/%s_business_area.txt" % response.meta["city"],"a")
                 
                fp.write(pos+"\n")
        