#!/bin/sh

alias mysql_dida='/usr/local/mysql/bin/mysql -h211.151.139.62 -ujiangyuanshu -pJiangyuanSHU didapinche'

mysql_dida -N -e "SELECT ride_id,start_city_id,start_lon,start_lat,end_lon,end_lat,distance_meters from ride_line where start_city_id=end_city_id 
ORDER BY ride_id desc limit 300000; " > sample/city_ride_tmp.txt

cat /dev/null > sample/city_percent.txt

arr=(1 2 3 4 15 16 17 18 19 37 38 40 41 42 46 50 51 52 53 54 55 60 61 62 63 65 67 97 112 129 146 167 236 265 266 267 322 333 339 365 1315)

#城市订单所占比例
for var in ${arr[@]};
do
	awk -v cityid=${var} 'BEGIN{count=0}{if($2==cityid) {count+=1;}}END{print cityid,count/300000}' sample/city_ride_tmp.txt >> sample/city_percent.txt
done

mysql_dida -N -e "SELECT start_lon,start_lat,end_lon,end_lat,distance_meters from ride_line where start_city_id!=end_city_id 
ORDER BY ride_id desc limit 10000;" > sample/country_ride.txt