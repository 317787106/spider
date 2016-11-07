#!/bin/sh

#线上-api
awk -F"\t" '{if($1==37 && ($6-$7)>10000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)>9000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)>8000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)>7000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)>6000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)>5000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)>4000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)>3000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)>2000) print}' test.txt | wc -l
echo ''

awk -F"\t" '{if($1==37 && ($6-$7)<-2000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)<=-3000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)<=-4000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)<=-5000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)<=-6000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)<=-7000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)<=-8000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)<=-9000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($6-$7)<=-10000) print}' test.txt | wc -l
echo ''

#计算-api
awk -F"\t" '{if($1==37 && ($8-$7)>10000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)>9000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)>8000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)>7000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)>6000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)>5000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)>4000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)>3000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)>2000) print}' test.txt | wc -l
echo ''

awk -F"\t" '{if($1==37 && ($8-$7)<=-2000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)<=-3000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)<=-4000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)<=-5000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)<=-6000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)<=-7000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)<=-8000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)<=-9000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$7)<=-10000) print}' test.txt | wc -l
echo ''

#计算-线上
awk -F"\t" '{if($1==37 && ($8-$6)>10000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)>9000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)>8000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)>7000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)>6000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)>5000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)>4000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)>3000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)>2000) print}' test.txt | wc -l
echo ''

awk -F"\t" '{if($1==37 && ($8-$6)<=-2000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)<=-3000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)<=-4000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)<=-5000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)<=-6000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)<=-7000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)<=-8000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)<=-9000) print}' test.txt | wc -l
awk -F"\t" '{if($1==37 && ($8-$6)<=-10000) print}' test.txt | wc -l
echo ''