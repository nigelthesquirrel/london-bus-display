#/bin/bash
unclutter -idle 1 -root &
cd /home/pi/london-bus-display
/usr/bin/python BusTimes.py > BusTimes.log 2>&1