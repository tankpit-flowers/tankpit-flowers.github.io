#!/bin/sh

SCRIPTDIR=/home/crosswalkcalvin/tankpit-flowers.github.io

python $SCRIPTDIR/scraper.py

cd $SCRIPTDIR

git add .
git commit -a -m "Automated commit triggered."
git push origin master
