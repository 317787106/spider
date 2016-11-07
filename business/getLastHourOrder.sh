#!/bin/sh

alias mysql_dida='/usr/local/mysql/bin/mysql -h192.168.2.57 -ujiangyuanshu -pJiangyuanSHU didapinche'

mysql_dida -N -e "
select r.plan_start_time,r.create_time,r.reply_time,l.start_lon,l.start_lat,l.end_lon,l.end_lat,r.id
from ride r
LEFT JOIN ride_line l on l.ride_id = r.id
where r.plan_start_time >= DATE_FORMAT(DATE_ADD(now(),INTERVAL -1 hour), '%Y-%m-%d %H') and r.plan_start_time < DATE_FORMAT(NOW(), '%Y-%m-%d %H')
and l.start_city_id=1 and l.end_city_id=1;" > order/beijing_order.txt

mysql_dida -N -e "
select r.plan_start_time,r.create_time,r.reply_time,l.start_lon,l.start_lat,l.end_lon,l.end_lat,r.id
from ride r
LEFT JOIN ride_line l on l.ride_id = r.id
where r.plan_start_time >= DATE_FORMAT(DATE_ADD(now(),INTERVAL -1 hour), '%Y-%m-%d %H') and r.plan_start_time < DATE_FORMAT(NOW(), '%Y-%m-%d %H')
and l.start_city_id=2 and l.end_city_id=2;" > order/shanghai_order.txt

mysql_dida -N -e "
select r.plan_start_time,r.create_time,r.reply_time,l.start_lon,l.start_lat,l.end_lon,l.end_lat,r.id
from ride r
LEFT JOIN ride_line l on l.ride_id = r.id
where r.plan_start_time >= DATE_FORMAT(DATE_ADD(now(),INTERVAL -1 hour), '%Y-%m-%d %H') and r.plan_start_time < DATE_FORMAT(NOW(), '%Y-%m-%d %H')
and l.start_city_id=3 and l.end_city_id=3;" > order/guangzhou_order.txt

mysql_dida -N -e "
select r.plan_start_time,r.create_time,r.reply_time,l.start_lon,l.start_lat,l.end_lon,l.end_lat,r.id
from ride r
LEFT JOIN ride_line l on l.ride_id = r.id
where r.plan_start_time >= DATE_FORMAT(DATE_ADD(now(),INTERVAL -1 hour), '%Y-%m-%d %H') and r.plan_start_time < DATE_FORMAT(NOW(), '%Y-%m-%d %H')
and l.start_city_id=4 and l.end_city_id=4;" > order/shenzhen_order.txt

mysql_dida -N -e "
select r.plan_start_time,r.create_time,r.reply_time,l.start_lon,l.start_lat,l.end_lon,l.end_lat,r.id
from ride r
LEFT JOIN ride_line l on l.ride_id = r.id
where r.plan_start_time >= DATE_FORMAT(DATE_ADD(now(),INTERVAL -1 hour), '%Y-%m-%d %H') and r.plan_start_time < DATE_FORMAT(NOW(), '%Y-%m-%d %H')
and l.start_city_id=37 and l.end_city_id=37;" > order/tianjin_order.txt