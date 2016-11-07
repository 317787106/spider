#!/bin/sh

#线上-api
awk -F"\t" '{if(($5-$6)>100000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)>90000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)>80000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)>70000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)>60000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)>50000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)>40000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)>30000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)>20000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)>10000) print}' test_country.txt | wc -l
echo ''

awk -F"\t" '{if(($5-$6)<=-10000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)<=-20000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)<=-30000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)<=-40000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)<=-50000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)<=-60000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)<=-70000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)<=-80000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)<=-90000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($5-$6)<=-100000) print}' test_country.txt | wc -l
echo ''

#计算-api
awk -F"\t" '{if(($7-$6)>100000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)>90000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)>80000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)>70000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)>60000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)>50000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)>40000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)>30000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)>20000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)>10000) print}' test_country.txt | wc -l
echo ''

awk -F"\t" '{if(($7-$6)<=-10000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)<=-20000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)<=-30000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)<=-40000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)<=-50000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)<=-60000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)<=-70000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)<=-80000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)<=-90000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$6)<=-100000) print}' test_country.txt | wc -l
echo ''

#计算-线上
awk -F"\t" '{if(($7-$5)>100000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)>90000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)>80000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)>70000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)>60000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)>50000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)>40000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)>30000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)>20000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)>10000) print}' test_country.txt | wc -l
echo ''

awk -F"\t" '{if(($7-$5)<=-10000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)<=-20000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)<=-30000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)<=-40000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)<=-50000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)<=-60000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)<=-70000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)<=-80000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)<=-90000) print}' test_country.txt | wc -l
awk -F"\t" '{if(($7-$5)<=-100000) print}' test_country.txt | wc -l
echo ''