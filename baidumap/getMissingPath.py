#encoding:utf-8

def getPidSet(cityid):
    lines = open('city_map/all_map_%s.txt' % cityid).readlines()
    pidset = set()
    for line in lines:
        pid = int(line.strip().split("\t")[0])
        pidset.add(pid)
        
    return pidset

def getPath(cityid):
    lines = open('city_map/all_map_%s_p2p.txt' % cityid).readlines()
    pid2pid = dict()
    for line in lines:
        items = line.strip().split("\t")
        pid1 = int(items[0])
        pid2 = int(items[1])
        if pid1 not in pid2pid:
            pid2pid[pid1] = set([pid2,])
        else:
            pid2pid[pid1].add(pid2)
        
    return pid2pid

def getMissingPath(cityid):    
    pidset = getPidSet(cityid)
    path = getPath(cityid)
    
    fp = open('missing_path_%s.txt' % cityid,'w')
    for pid1 in pidset:
        line = [str(pid1),]
        for pid2 in pidset:
            if (pid1 not in path or pid2 not in path[pid1]) and pid1 != pid2:
                line.append(str(pid2))
        if len(line)>1:
            fp.write("\t".join(line)+"\n")
            
def getSingleRouteMissingPath():    
    pidset = getPidSet(0)
    path = getPath(0)
    
    fp = open('missing_path.txt','w')
    for pid1 in pidset:
        line = [str(pid1),]
        #全部遗漏
        if pid1 not in path:
            for pid in pidset:
                if pid>pid1:
                    line.append(str(pid))
        else:
            for pid in pidset:
                if pid1 < pid:
                    #部分遗漏
                    if pid not in path[pid1]:
                        line.append(str(pid))
        if len(line)>1:
            fp.write("\t".join(line)+"\n")
                
if __name__ == "__main__":
    #getSingleRouteMissingPath()
    #for cityid in [1,2,3,4,15,16,17,18,19,37,38,40,41,42,46,50,51,52,53,54,55,60,61,62,63,65,67,97,112,129,146,167,236,265,266,267,322,333,339,365,1315]:
    for cityid in [2,]:
        getMissingPath(cityid)
        