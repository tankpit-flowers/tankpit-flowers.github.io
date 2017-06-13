#!/bin/sh

PYTHONBIN=/home/ec2-user/anaconda2/bin/python
SCRIPTDIR=/home/ec2-user/tax

cd $SCRIPTDIR

git reset --hard
git pull

$PYTHONBIN $SCRIPTDIR/scraper.py

git add .
git commit -a -m "Automated commit triggered."
git push origin master
