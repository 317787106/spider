#encoding:utf-8

from elasticsearch import Elasticsearch
from datetime import datetime,timedelta
from posInPolygon import Point,cityid2name,getDistrict2Polygon,getPointWithDistrict

def writePosIntoEs(startOrEnd):
    '''把每个订单的起点位置、终点位置转换成商圈，然后写入es
    '''
    es=Elasticsearch('192.168.2.183')
    
    for cityid in [1,2,3,4,37]:
        district2Polygon = getDistrict2Polygon(cityid)
        
        for line in open("order/%s_order.txt" % cityid2name[cityid]).readlines():

            items = line.strip().split("\t")
            
            if startOrEnd == "start":
                p = Point(float(items[3]),float(items[4]))
            elif startOrEnd == "end":
                p = Point(float(items[5]),float(items[6]))
            
            distircts = getPointWithDistrict(p,district2Polygon)
            
            if len(distircts) == 0:
                continue
            
            plan_start_time = datetime.strptime(items[0],'%Y-%m-%d %H:%M:%S') - timedelta(hours=8)
            create_time = datetime.strptime(items[1],'%Y-%m-%d %H:%M:%S') - timedelta(hours=8)
            replied = 1 if items[2] != "NULL" else 0
            rideid = int(items[7])
            
            for distirct in distircts:
                
                data = {"plan_start_time":plan_start_time.strftime('%Y-%m-%dT%H:00:00'),
                        "create_time":create_time.strftime('%Y-%m-%dT%H:00:00'),
                        "replied": replied,
                        "business":distirct,
                        "cityid":cityid,
                        "rideid":rideid
                        }
                
                if startOrEnd == "start":
                    es.index(index='business',doc_type='startpos',body=data)
                elif startOrEnd == "end":
                    es.index(index='business',doc_type='endpos',body=data)
        
        print "%s cityid:%s ok!" % (startOrEnd,cityid)
                    
if __name__ == "__main__":
    writePosIntoEs("start")
    writePosIntoEs("end")