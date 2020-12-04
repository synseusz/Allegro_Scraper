#!/bin/bash

date
cd /home/pi/Projects/Python
cp ./listed_items.csv ./listed_items_prev.csv
./allegro_scraper.py
echo
exit
