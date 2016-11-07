# encoding: utf-8

from __future__ import division
import math

EARTH_RADIUS = 6378137

def rad(pos):
    return pos * math.pi / 180.0;

#第一个点的经度、纬度，第二个点的经、度纬度
def getDistanceByPosition(longitude1,latitude1,longitude2,latitude2):
    
    red_lat1 = rad(latitude1)
    red_lat2 = rad(latitude2)
    
    diff_lat = red_lat1 - red_lat2
    diff_long = rad(longitude1) - rad(longitude2)
    
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(diff_lat/2),2)+math.cos(red_lat1)*math.cos(red_lat2)*math.pow(math.sin(diff_long/2),2)));  
    s *= EARTH_RADIUS
    
    return s

def getDistanceByTwoPosition(position1,position2):
    return getDistanceByPosition(position1[0],position1[1],position2[0],position2[1])

def getManhattanDistince(longitude1,latitude1,longitude2,latitude2):
    offset_x = abs(longitude1-longitude2) * math.pi/180 * EARTH_RADIUS/1000
    offset_y = abs(latitude1-latitude2) * math.pi/180 * EARTH_RADIUS/1000

    return int(math.floor((offset_x+offset_y)*1000))
    
def getManhattanDistanceByTwoPosition(position1,position2):
    return getManhattanDistince(position1[0],position1[1],position2[0],position2[1])
    
def getAverageCicle(pos_array):
    longitude_center = float(0.0)
    latitude_center = float(0.0)
    
    for i in range(0,len(pos_array)):
        longitude_center += pos_array[i][0]
        
    longitude_center /= len(pos_array)
    
    for i in range(0,len(pos_array)):
        latitude_center += pos_array[i][1]
        
    latitude_center /= len(pos_array)
    
    distances = list()
    
    for i in range(0,len(pos_array)):
        distance = getDistanceByPosition(pos_array[i][0],pos_array[i][1],longitude_center,latitude_center)
        distances.append(distance)
    
    max_distance = max(distances)
    
    return max_distance

if __name__ == "__main__":
    #print getDistanceByPosition(115.459545,39.467721,117.133582,39.467721) #东西长
    #print getDistanceByPosition(115.459545,39.467721,115.459545,41.028924) #南北宽
    #print getDistanceByPosition(116.156912,39.742562,116.694880,39.742562) #东西长
    #print getDistanceByPosition(116.156912,39.742562,116.156912,40.178154) #南北宽
    
    #116.464950    39.962039    116.844702    39.964892
    #116.489321    39.974335    116.552732    40.043747
    #print getManhattanDistanceByTwoPosition((116.42307,40.07037),(116.48803,40.00231))
    print getDistanceByTwoPosition((116.48609699999999,40.000651),(116.486497,40.001051))
    #print getManhattanDistanceByTwoPosition((116.46198,39.87544),(116.48802,39.95042))
    #print getDistanceByTwoPosition((116.46198,39.87544),(116.48802,39.95042))
    
    