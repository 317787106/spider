#encoding:utf-8

if __name__ == "__main__":

    content = ''.join([line.rstrip()+" " for line in open("all_map_data_folder/322_crossing_src.txt").readlines()])
    print content
    lines = content.split(";")
    fp =  open("all_map_data_folder/322_crossing.txt","w")
    for line in lines:
        line = line.strip()
        
        items = line.split()
        print items[0],items[1],items[2]
        fp.write("{0}\t{1}\t{2}\n".format(items[0],items[1],items[2]))