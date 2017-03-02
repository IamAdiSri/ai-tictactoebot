#!/bin/bash
cd ou_v1
for i in 1 2 3 4 5 6 7 8 9 10
do
    touch $i 
    python ../team52.py 3 > $i
done