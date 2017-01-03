#encoding:utf-8

from __future__ import division

cityid2name = {1:"beijing",
               2:"shanghai",
               3:"guangzhou",
               4:"shenzhen",
               37:"tianjin"
               }

class Point:
    def __init__(self,lon,lat):
        self.lon = lon
        self.lat = lat

'''判断点p是否在多边形polygon内
'''
def pointInPolygon(p,polygon):
    nCount = len(polygon)
    nCross = 0

    for i in range(0,nCount):
        p1 = polygon[i]
        p2 = polygon[(i+1) % nCount]
        
        #求解 y=p.y 与 p1p2 的交点
        if p1.lat == p2.lat:    #p1p2 与 y=p0.y平行 
            continue
        if p.lat < min(p1.lat,p2.lat): #交点在p1p2延长线上
            continue
        if p.lat >= max(p1.lat,p2.lat): #交点在p1p2延长线上
            continue
        
        #求交点的 X 坐标 
        x = (float)(p.lat - p1.lat) * (float)(p2.lon - p1.lon) / (float)(p2.lat - p1.lat) + p1.lon;
        if x > p.lon: 
            nCross += 1  #只统计单边交点 
            
    return nCross % 2 == 1

def getDistrict2Polygon(cityid):
    district2Polygon = dict()
    
    cityname = cityid2name[cityid]
    lines = open("area/"+cityname+"_business_area.txt").readlines()
    #lines.extend(open("area/"+cityname+"_college_area.txt").readlines())
    
    for line in lines:
        items = line.strip().split("\t")
        
        points = items[1].strip(";").split(";")
    
        polygon = []
        for point in points:
            data = point.split(",")
            p = Point(float(data[0]),float(data[1]))
            polygon.append(p)
        
        district2Polygon[items[0]] = polygon
        
    return district2Polygon
    
def getPointWithDistrict(p,district2Polygon):
    districts = []
    for district,polygon in district2Polygon.iteritems():
        if pointInPolygon(p,polygon) == True:
            districts.append(district)
    
    return districts
    
    

def test(): 
    district2count = dict()
    
    cityid = 37
    district2Polygon = getDistrict2Polygon(cityid)
    
    count = 0
    for line in open("area/%s_order.txt" % cityid2name[cityid]).readlines():
        if count % 1000 == 0:
            print count
        count += 1
        
        items = line.strip().split("\t")
        
        p = Point(float(items[0]),float(items[1]))
        
        distircts = getPointWithDistrict(p,district2Polygon)
        
        for distirct in distircts:
            if distirct not in district2count:
                district2count[distirct] = 1
            else:
                district2count[distirct] += 1
                
    district2count_list = sorted(district2count.iteritems(),key=lambda d:d[1],reverse=False)
    
    for item in district2count_list:
        print "%s\t%s" % (item[0],item[1])
        
def getArea2User():
    area = "116.480315902,40.0072116508;116.480471398,40.0073117506;116.48073029,40.0073847011;116.481281041,40.0074122647;116.48157299,40.0074325057;116.482020526,40.0074630399;116.482341581,40.0074932977;116.482789835,40.0075179598;116.484107739,40.0076072134;116.484862675,40.007630563;116.485033353,40.0075501519;116.485197833,40.0048122512;116.48500344,40.0046712496;116.484518894,40.0046013359;116.48392197,40.0044618538;116.483576751,40.0043372246;116.483426644,40.0042874144;116.483092923,40.0041429574;116.482894937,40.004054183;116.482469769,40.0037883424;116.481465733,40.0037592574;116.47854076,40.0056077543;116.480319495,40.0072180064;116.480315902,40.0072116508"
    points = area.split(";")
    
    polygon = []
    for point in points:
        p = Point(float(point.split(",")[0]),float(point.split(",")[1]))
        polygon.append(p)
        
    count = 0
    with open("beijing_user_active_uniq.txt") as f:
        for line in f:
            data = line.strip().split("\t")
            p = Point(float(data[1]),float(data[2]))
            
            if pointInPolygon(p,polygon):
                count +=1
    print count
                    
if __name__ == "__main__":
    getArea2User()
    