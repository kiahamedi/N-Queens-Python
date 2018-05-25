#!/bin/bash
python get_redis.py | tr 'b' ' ' | tr -d "'" | cut -d: -f1 > duplicate.dat
python get_redis.py | tr 'b' ' ' | tr -d "'" | cut -d: -f2 > fitnes.dat
#plot 'duplicate.dat' with linespoints ls 2 ,'fitnes.dat' with linespoints ls 1
