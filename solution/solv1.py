#!/usr/bin/python3
"""
This module implements first solution, based on "DFS" and simulation of time.

It uses picosat (picosat can also detect multiple solutions).
"""

import common
from common import HumanReadableOutput
import subprocess

def errprint(*args):
    """General debug messages."""
    common.errprint("solv1.py: ", *args)

class SATProgram:
    numberOfVariables = 0
    numberOfLines = 0
    clauses = None

    def __init__(self, _numvar, _numclauses, _clauses):
        self.numberOfVariables = _numvar
        self.numberOfClauses = _numclauses
        self.clauses = _clauses
        if len(self.clauses) != _numclauses:
            raise Exception("_numclauses != len(_clauses)")
        for clause in self.clauses:
            for x in clause:
                if not 1 <= abs(x) <= _numvar:
                    raise Exception("incorrect variable")

    def programRerp(self):
        lines = []
        lines.append("p cnf {0} {1}".format(self.numberOfVariables, self.numberOfClauses))
        for clause in self.clauses:
            lines.append(" ".join([str(x) for x in clause]))
        return "\n".join(lines)

    def addClause(self, clause):
        maxVariable = max([abs(x) for x in clause])
        self.numberOfVariables = max(maxVariable, self.numberOfVariables)
        self.numberOfClauses += 1
        self.clauses.append(clause)

    def addClauses(self, clauses):
        for clause in clauses:
            self.addClause(clause)
        
def productSATProgram(rawInput):
    # @TODO
    
    # variables:
    # amount of walls
    # + trivial true
    # + wall x time

    return SATProgram(0, 0, [])

def applySATSolver(program):
    # @TODO
    return []

def convertToHumanReadableOutput(rawInput, rawOutput):
    # @TODO
    return HumanReadableOutput(rawInput, [])

def solve(rawInput):
    # @TODO
    errprint("Starting...")
    program = productSATProgram(rawInput)
    rawOutput = applySATSolver(program)
    output = convertToHumanReadableOutput(rawInput, rawOutput)
    errprint("Finishing...")
    return output
