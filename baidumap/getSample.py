#encoding:utf-8
from random import sample

'''分城市随机抽样'''
def sample_city():
    
    city2orders = dict()
    cityids = [1,2,3,4,15,16,17,18,19,37,38,40,41,42,46,50,51,52,53,54,55,60,61,62,63,65,67,97,112,129,146,167,236,265,266,267,322,333,339,365,1315]
    
    with open("sample/city_ride_tmp.txt") as f:
        for line in f:
            items = line.strip().split()
            cityid = int(items[1])
            
            if cityid in cityids:
                order = "\t".join(items[1:])
                if cityid not in city2orders:
                    city2orders[cityid] = [order,]
                else:
                    city2orders[cityid].append(order)
                
    fp = open("sample/city_ride.txt","w")        
    for cityid in city2orders:
        orders = city2orders[cityid]
        
        sample_size = 1000
        if len(orders) <= 1000:
            sample_size = len(orders)
            
        orders = sample(orders,sample_size)
        
        for order in orders:
            fp.write(order+"\n")
    fp.close()
    
'''不分城市随机抽样'''
def sample_ride():        
    
    samples = []
    with open("sample/city_ride_tmp.txt") as f:
        for line in f:
            line = line.strip()
            samples.append(line)
    fp = open("sample/sample_ride.txt","w")
    samples = sample(samples,10000)
    for order in samples:
        fp.write(order+"\n")
    fp.close()
            
if __name__ == "__main__":
    #sample_city()
    sample_ride()