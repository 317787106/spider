#!/bin/sh

alias mysql_dida='/usr/local/mysql/bin/mysql -h192.168.2.57 -ujiangyuanshu -pJiangyuanSHU didapinche'

#按商圈拆分的订单
sites=("1 beijing" "2 shanghai" "3 guangzhou" "4 shenzhen" "37 tianjin")
n_sites=${#sites[*]} 
for ((i=0;i<$n_sites;i++));
do
    inner_sites=(${sites[$i]}) #将一维sites字符串赋值到数组

	mysql_dida -N -e "
	select r.plan_start_time,r.create_time,r.reply_time,l.start_lon,l.start_lat,l.end_lon,l.end_lat,r.id
	from ride r
	LEFT JOIN ride_line l on l.ride_id = r.id
	where r.plan_start_time >= DATE_FORMAT(DATE_ADD(now(),INTERVAL -1 hour), '%Y-%m-%d %H') and r.plan_start_time < DATE_FORMAT(NOW(), '%Y-%m-%d %H')
	and l.start_city_id=${inner_sites[0]} and l.end_city_id=${inner_sites[0]};" > order/${inner_sites[1]}_order.txt

done

#按六边形拆分的订单
mysql_dida -N -e "
select r.plan_start_time,r.create_time,r.reply_time,l.start_lon,l.start_lat,l.end_lon,l.end_lat,r.id,
l.start_city_id,l.distance_meters,r.suggest_price,r.price-r.suggest_price,r.initiator_user_id,r.driver_user_id
from ride r
LEFT JOIN ride_line l on l.ride_id = r.id
where r.plan_start_time >= DATE_FORMAT(DATE_ADD(now(),INTERVAL -1 hour), '%Y-%m-%d %H') and r.plan_start_time < DATE_FORMAT(NOW(), '%Y-%m-%d %H')
and r.ride_type!=7;" > order/all_city_order.txt