#!/bin/bash
for i in 1 2 13 4 15 6 7 8 9 0
do
    touch $i 
    python team52.py 2 > $i
done