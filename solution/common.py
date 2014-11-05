#!/usr/bin/python3
"""
This module defines common structures and functions, used throughout the whole project.
"""

import sys

def errprint(*args):
    print(*args, file=sys.stderr)

class RawInput:
    numberOfRows = 0
    numberOfColumns = 0
    grid = []

    def __init__(self, rows, columns, grid):
        self.numberOfRows = rows
        self.numberOfColumns = columns
        self.grid = grid

    def __str__(self):
        return "\n".join(["\t".join([str(x) for x in line]) for line in self.grid])

class HumanReadableOutput:
    numberOfRows = 0
    numberOfColumns = 0
    walls = []
    rawInput = None

    def __init__(self, rawInput, walls):
        self.numberOfRows = rawInput.numberOfRows
        self.numberOfColumns = rawInput.numberOfColumns
        self.walls = walls
        self.rawInput = rawInput

    def __str__(self):
        """ This representation goes on output.
        """
        # @TODO
        return str(self.walls)

    def ASCIIrepr(self):
        # @TODO
        return "ASCII come soon " + str(self)
