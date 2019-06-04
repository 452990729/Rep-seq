#!/bin/bash
file=$1
cpu=$2
prefix=$3
[ ! $2 ] && cpu=2

bsub -n $cpu  -q normal -o $prefix.log -e  $prefix.e sh $1

tmp=`bjobs -w|grep ${prefix}|awk '{print $1}'`
#tmp=`bjobs|grep ${prefix}|awk '{print $1}'`
#echo "$tmp"X
while [ "$tmp"X != ""X ]
do
  sleep 10
  tmp=`bjobs -w|grep ${prefix}|awk '{print $1}'`
  #tmp=`bjobs|grep ${prefix}|awk '{print $1}'`
done

echo "All $prefix jobs had been finished"


