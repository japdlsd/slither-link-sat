#!/bin/bash

for i in ../tests/*; do
    echo $i
    ./main.py < $i
done
