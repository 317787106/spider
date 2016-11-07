#encoding:utf-8

from business.posInPolygon import Point,pointInPolygon
import math
import re

def split_city(cityid):
    '''把城市按边界分块
    '''
    
    polygon = []
    
    for point in open("city_border/%s.txt" % cityid).readlines():
        data = point.split()
        p = Point(float(data[0]),float(data[1]))
        polygon.append(p)
        
    min_lon = min([point.lon for point in polygon])
    max_lon = max([point.lon for point in polygon])
    min_lat = min([point.lat for point in polygon])
    max_lat = max([point.lat for point in polygon])
    
    step = 0.02
    lon_step = int(math.ceil((max_lon-min_lon)/step))
    lat_step = int(math.ceil((max_lat-min_lat)/step))
    
    fp = open("city_border/parts_%s.txt" % cityid,"w")
    
    for i in range(lon_step):
        for j in range(lat_step):
            leftdown_point = Point(min_lon+i*step,min_lat+j*step)
            rightup_point = Point(min_lon+(i+1)*step,min_lat+(j+1)*step)
            
            if pointInPolygon(leftdown_point,polygon) or pointInPolygon(rightup_point,polygon):
                fp.write("{0},{1},{2},{3}\n".format(leftdown_point.lat,leftdown_point.lon,rightup_point.lat,rightup_point.lon))
                
    #print min_lon,max_lon,min_lat,max_lat
    
def text_format(cityid):
    '''清洗poi的原始数据文件，并做初步分类
    '''
    fp = open("keypoints/point_%s.format" % cityid,"w")
    
    with open("keypoints/point_%s.txt" % cityid) as f:
        for line in f:
            
            items = line.strip().split("\t")
            
            #重复的交叉路口
            if "路口" in items[3] and "/" not in items[3] and "路" not in items[4]:
                continue
            
            
            m = re.search("地铁", items[3])
            if m:
                poi_type = 1
                if items[3].find("便利店") !=-1 or items[3].find("(") !=-1:
                    poi_type = 5 #过小的楼
            else:
                m = re.search("\d+路", items[4])
                if m:
                    items[3] = items[3] +"(公交站)"
                    poi_type = 2
                else:
                    m = re.search("路口", items[3])
                    if m:
                        poi_type = 3
                    else:
                        m = re.search("门", items[3])
                        if m:
                            poi_type = 4
                            if items[3].find("号楼") !=-1:
                                poi_type = 41 #过小的楼
                        else:
                            poi_type = 5 #默认为地标建筑或者商店

            
            items[5] = str(poi_type)
            
            fp.write("\t".join(items)+"\n")
    
    fp.close()
    
def convertTojs(cityid):
    '''把format文件转换成javascript能识别的格式
    '''
    fp = open("keypoints/point_%s.js" % cityid,"w")
    
    jsstring = '''var data = {"data":['''
    with open("keypoints/point_%s.format" % cityid) as f:
        for line in f:
            items = line.strip().split("\t")
            jsstring += "[%s,%s,'%s']," % (items[1],items[2],items[3].replace("'"," "))
    
    jsstring = jsstring.rstrip(",")
    jsstring += "]}"
    
    fp.write(jsstring)
    fp.close()

if __name__ == "__main__":
#     for cityid in [15,16,17,18,19,38,40,41,46,50,51,52,53,54,55,60,61,62,65,67,97,112,129,146,167,236,265,266,267,322,333,339,365,1315]:
#     #for cityid in [1,2,3,4,15,16,17,18,19,37,38,40,41,42,46,50,51,52,53,54,55,60,61,62,63,65,67,97,112,129,146,167,236,265,266,267,322,333,339,365,1315]:
#         split_city(cityid)
#         print cityid," complete !"
    #for cityid in [42,]:
    for cityid in [1,2,3,4,15,16,17,18,19,37,38,40,41,42,46,50,51,52,53,54,55,60,61,62,63,65,67,97,112,129,146,167,236,265,266,267,322,333,339,365,1315]:
        text_format(cityid)
        convertTojs(cityid)