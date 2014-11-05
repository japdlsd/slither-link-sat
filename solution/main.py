#!/usr/bin/python3
"""
This module takes care about communication with outer world. It reads
problem raw representation, it outputs human-readable solution.

It should be written in such a way that it is easy to change implementation of 
individual steps of solution.
"""

import common
from common import RawInput
from solv1 import solve

def errprint(*args):
    """General debug messages."""
    common.errprint("main.py: ", *args)

def readProblemInstance():
    R, C = [int(x) for x in input().split(" ")][:2]
    grid = []
    for r in range(R):
        grid.append([int(x) for x in input().split(" ")][:C])
    return RawInput(R, C, grid)

if __name__ == "__main__":
    errprint("Starting...")

    rawInput = readProblemInstance()
    errprint("rawInput:\n", rawInput)

    output = solve(rawInput)

    print(output)
    errprint("solution ASCII prepresentation: \n", output.ASCIIrepr())
