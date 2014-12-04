#!/bin/bash
for i in tests/*.in; do
    echo $i
    python3 solution/main.py < $i
done
