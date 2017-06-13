#!/bin/sh

SCRIPTDIR=/home/ec2-user/tax

DATESTRING=$(date +%Y-%m-%d) # 2017-01-01

cp $SCRIPTDIR/data/flowers_stats_daily.csv $SCRIPTDIR/data/flowers_stats_archive/flowers_stats_$DATESTRING.csv
cp $SCRIPTDIR/data/flowers_stats_now.csv $SCRIPTDIR/data/flowers_stats_daily.csv

cp $SCRIPTDIR/data/flowers_hours_log.csv $SCRIPTDIR/data/flowers_hours_log_backups/flowers_hours_log_$DATESTRING.csv

cp $SCRIPTDIR/index.md $SCRIPTDIR/backups/index/index-$DATESTRING.md
cp $SCRIPTDIR/stats.md $SCRIPTDIR/backups/stats/stats-$DATESTRING.md
cp $SCRIPTDIR/stats-kills.md $SCRIPTDIR/backups/stats/stats-kills-$DATESTRING.md
cp $SCRIPTDIR/stats-deact.md $SCRIPTDIR/backups/stats/stats-deact-$DATESTRING.md
cp $SCRIPTDIR/activity.md $SCRIPTDIR/backups/activity/activity-$DATESTRING.md
cp $SCRIPTDIR/activity-week.md $SCRIPTDIR/backups/activity/activity-week-$DATESTRING.md
cp $SCRIPTDIR/activity-month.md $SCRIPTDIR/backups/activity/activity-month-$DATESTRING.md

cd $SCRIPTDIR

git add .
git commit -a -m "Automated daily backup triggered."
git push origin master

