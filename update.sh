#!/bin/sh

SCRIPTDIR=/home/crosswalkcalvin/tankpit-flowers.github.io

cd $SCRIPTDIR

git reset --hard
git pull

python $SCRIPTDIR/scraper.py

git add .
git commit -a -m "Automated commit triggered."
git push origin master
