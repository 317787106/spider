#encoding:utf-8

'''
城市地图增删点后，已有的点存放于all_map_x01.txt中，已有的路径存放于all_map_x01_p2p.txt中，新增加的点存放于all_map_x02.txt中；
后续抓取x02*x02,part1*part2,part2*part1即可
'''
def getp2pMap(cityid):
    
    src_pos2pid = dict()
    for line in open("city_map/all_map_%s.txt" % cityid).readlines():
        items = line.strip().split("\t")
        pid = int(items[0])
        pos = "%s_%s" % (items[1],items[2])
        
        src_pos2pid[pos] = pid
        
    new_pos2pid = dict()
    for line in open("city_map/all_map_%s_new.txt" % cityid).readlines():
        items = line.strip().split("\t")
        pid = int(items[0])
        pos = "%s_%s" % (items[1],items[2])
        
        new_pos2pid[pos] = pid
        
    exist_pidset = set() #存放old_pid
    p2p_map = dict()
    
    fp1 = open("city_map/all_map_%s01.txt" % cityid,"w") #已有的点
    fp2 = open("city_map/all_map_%s02.txt" % cityid,"w") #新添加的点
    for pos,new_pid in new_pos2pid.items():
        items = pos.split("_")
        
        if pos in src_pos2pid:
            old_pid = src_pos2pid[pos]
            p2p_map[old_pid] = new_pid
            exist_pidset.add(old_pid)
            
            fp1.write("%s\t%s\t%s\n" % (new_pid,items[0],items[1]))
        else:
            fp2.write("%s\t%s\t%s\n" % (new_pid,items[0],items[1]))
    
    fp1.close()
    fp2.close()        
            
    #p2p.txt中只保留exist_pidset点的映射，并替换成新的pid
    print len(exist_pidset)
    fp = open("city_map/all_map_%s01_p2p.txt" % cityid,"w")
    for line in open("city_map/all_map_%s_p2p.txt" % cityid).readlines():
        items = line.strip().split("\t")
        pid1 = int(items[0])
        pid2 = int(items[1])
        distance = int(items[2])
        if pid1 in exist_pidset and pid2 in exist_pidset:
            pid1_new = p2p_map[pid1]
            pid2_new = p2p_map[pid2]
            fp.write("%s\t%s\t%s\n" % (pid1_new,pid2_new,distance))
            
    fp.close()
    
    
if __name__ == "__main__":
    getp2pMap(2)