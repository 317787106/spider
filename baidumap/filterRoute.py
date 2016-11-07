#encoding:utf-8

'''计算城市地图中任意2点来回路线的较小距离'''
def getMinPathBetweenPointInCity(cityid):
    
    p2p_distance = dict()
    
    with open('city_map/all_map_%s_p2p.txt' % cityid) as f:
        for line in f:
            items = line.split("\t")
            start_point_id = int(items[0])
            end_point_id = int(items[1])
            distance = int(items[2])
            
            lineno = (start_point_id,end_point_id) if start_point_id <= end_point_id else (end_point_id,start_point_id)
            
            if lineno not in p2p_distance:
                p2p_distance[lineno] = distance
            else:
                if distance < p2p_distance[lineno]:
                    p2p_distance[lineno] = distance
                    
    fp = open('city_map/all_map_%s_routine.txt' % cityid,'w')
    
    for lineno,distance in p2p_distance.iteritems():
        fp.write("{0}\t{1}\t{2}\n".format(lineno[0],lineno[1],distance))
    
    fp.close()
    
if __name__ == "__main__":
    #getRoutine()
    #for city_id in [1,2,3,4,15,16,17,18,19,37,38,40,41,42,46,50,51,52,53,54,55,60,61,62,63,65,67,97,112,129,146,167,236,265,266,267,322,333,339,365,1315]:
    for city_id in [2,]:
        getMinPathBetweenPointInCity(city_id)
        print "city_id %s ok!" % city_id
    