#!/bin/sh

SCRIPTDIR=/home/crosswalkcalvin/tankpit-flowers.github.io

DATESTRING=$(date +%Y-%m-%d) # 2017-01-01

cp $SCRIPTDIR/data/flowers_stats_daily.csv $SCRIPTDIR/data/flowers_stats_$DATESTRING.csv
cp $SCRIPTDIR/data/flowers_stats_now.csv $SCRIPTDIR/data/flowers_stats_daily.csv

cp $SCRIPTDIR/data/flowers_hours_log.csv $SCRIPTDIR/data/flowers_hours_log_backup_$DATESTRING.csv

cp $SCRIPTDIR/index.md $SCRIPTDIR/backups/index_backup_$DATESTRING.md
cp $SCRIPTDIR/stats.md $SCRIPTDIR/backups/stats_backup_$DATESTRING.md
cp $SCRIPTDIR/activity.md $SCRIPTDIR/backups/activity_backup_$DATESTRING.md