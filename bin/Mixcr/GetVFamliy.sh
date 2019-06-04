#!/usr/bin/env bash

sum=`cut -f 10 $1 | awk '{if (NR>1) print $0}' |sort |uniq -c | awk 'BEGIN{sum=0} {sum=sum+$1} END{print sum}'`

cut -f 10 $1 | awk '{if (NR>1) print $0}' |sort |uniq -c | awk -v sum="$sum" '{print $2"\t"$1"\t"$1/sum}'

