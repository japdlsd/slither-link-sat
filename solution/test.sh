#!/bin/bash

for i in ../tests/*; do
    echo $i
    python3 ./main.py < $i
done
