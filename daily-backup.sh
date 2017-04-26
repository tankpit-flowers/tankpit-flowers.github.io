#!/bin/sh

SCRIPTDIR=/home/crosswalkcalvin/tankpit-flowers.github.io

DATESTRING=$(date +%Y-%m-%d) # 2017-01-01

cp $SCRIPTDIR/data/flowers_stats_daily.csv $SCRIPTDIR/data/flowers_stats_$DATESTRING.csv
cp $SCRIPTDIR/data/flowers_stats_now.csv $SCRIPTDIR/data/flowers_stats_daily.csv