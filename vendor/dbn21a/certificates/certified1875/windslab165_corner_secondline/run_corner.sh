#!/bin/bash
# run_corner.sh TAG Xnum Xden y t N  -- march one corner in 20000-n chunks
set -e
TAG=$1; XN=$2; XD=$3; Y=$4; T=$5; N=$6
cd "$(dirname "$0")"
mkdir -p runs
lo=1
while [ $lo -le $N ]; do
  hi=$((lo+19999)); [ $hi -gt $N ] && hi=$N
  /usr/bin/python3 windrect_corner_iv.py corner $XN $XD "$Y" "$T" $N $lo $hi \
      runs/${TAG}_${lo}_${hi}.json >> runs/${TAG}.log 2>&1
  lo=$((hi+1))
done
echo DONE_$TAG >> runs/${TAG}.log
