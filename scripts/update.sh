#!/bin/sh
echo 'Pulling Fira Code sources...'
cd input/fira
git pull
echo 'Pulling IBM Plex sources...'
cd ../plex
git pull
echo 'Rebuilding ligatures...'
cd ../..
python3 src/collect.py