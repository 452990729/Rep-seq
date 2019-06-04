#!/bin/bash
file=$1
cpu=$2
prefix=$3
[ ! $2 ] && cpu=2

name=`basename $3`
run_path="bsub.$name"
[ -d $run_path ] || `mkdir $run_path`
cd $run_path
nu=1

cat $file | grep -v ^# | grep -v ^$ | while  read -r line
#cat $file|while read -r line
do
    if [[ $line =~ ".sh" ]]; then
        echo "sh $line" >$prefix.$nu.sh
    else
        echo "$line" >$prefix.$nu.sh
    fi
	bsub -n $cpu  -q normal -o $prefix.$nu.log -e  $prefix.$nu.e sh $prefix.$nu.sh
	nu=$(($nu+1))
done

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


