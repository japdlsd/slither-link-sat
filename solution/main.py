#!/usr/bin/python3

import itertools
import subprocess

def readTaskFromInput():
    numberOfRows, numberOfColumns = [int(x) for x in input().split(" ")]
    grid = [ [int(x) for x in input().split(" ")] for i in range(numberOfRows)]
    return (numberOfRows, numberOfColumns, grid)

class VDC:
    """Variable decoder.
    """
    def __init__(self, rawInput):
        self.numberOfColumns, self.numberOfRows, self.grid = rawInput
        self.amountOfVerticalWalls = (self.numberOfColumns + 1) * self.numberOfRows
        self.amountOfHorizontalWalls = (self.numberOfRows + 1) * self.numberOfColumns

    def wallIsInRange(self, row, column, orientation):
        if row < 0 or column < 0: return False
        if row > self.numberOfRows or column > self.numberOfColumns: return False
        if orientation == 0 and row == self.numberOfRows: return False
        if orientation == 1 and column == self.numberOfColumns: return False
        return True

    def wall(self, row, column, orientation):
        """ `orientation` 0 - vertical, 1 - horizontal
        """
        assert(orientation in (0,1))
        assert(self.wallIsInRange(row, column, orientation))
        if orientation == 0: return 1 + column * self.numberOfRows + row
        if orientation == 1: return 1 + self.amountOfVerticalWalls + row * self.numberOfColumns + column
    
    def vTrue(self):
        return 1 + self.amountOfVerticalWalls + self.amountOfHorizontalWalls

    def vFalse(self):
        return -self.vTrue()

    def rcoFromWall(self, w):
        w -= 1
        assert(w < self.amountOfVerticalWalls + self.amountOfHorizontalWalls)
        if w < self.amountOfVerticalWalls:
            orientation = 0
            column, row = w // numberOfRows, w % numberOfRows
            return (row, column, orientation)
        else:
            w = w - self.amountOfVerticalWalls
            orientation = 1
            row, column = w // numberOfColumns, w % numberOfColumns
            return (row, column, orientation)

    def cellWalls(self, row, column):
        return [self.wall(row, column, 0), self.wall(row, column, 1), self.wall(row+1, column, 1), self.wall(row, column+1, 0)]
    
    def nodeWalls(self, row, column):
        possibleWalls = [(row, column, 0), (row, column, 1), (row-1, column, 0), (row, column-1, 1)]
        res = [self.wall(*w) for w in possibleWalls if self.wallIsInRange(*w)]
        assert(len(res) >= 2)
        return res

    def atMostN(self, vs, n):
        # at least one from n+1 variables are false
        return [[-c for c in cs] for cs in itertools.combinations(vs, n+1)]

    def atLeastN(self, vs, n):
        # at most N - n variables are false
        # so at least one from N - n + 1 is true
        return [list(cs) for cs in itertools.combinations(vs, len(vs) - n + 1)]

    def exactlyN(self, vs, n):
        return self.atMostN(vs, n) + self.atLeastN(vs, n)
    
    def zeroOrTwo(self, vs):
        """Full CNF computation.
        """ 
        res = []
        for cs in itertools.product(range(2), repeat=len(vs)):
            if sum(cs) not in (0, 2):
                res.append([(-1)**c * v for (c, v) in zip(cs, vs)])
        return res


def rawInputToCNF(rawInput):
    numberOfRows, numberOfColumns, grid = rawInput
    clauses = []
    
    def addClauses(cs):
        assert([] not in cs)
        nonlocal clauses
        for c in cs: clauses.append(c)
    
    def normalizeClauses():
        """Delete redundant clauses.
        """
        nonlocal clauses
        clauses = [list(clause) for clause in list(set([tuple(sorted(clause)) for clause in clauses]))]
    
    vdc = VDC(rawInput)

    # Number of walls
    for i in range(numberOfRows):
        for j in range(numberOfColumns):
            if grid[i][j] != -1: 
                addClauses(vdc.exactlyN(vdc.cellWalls(i,j), grid[i][j]))
    
    # Connectivity
    for i in range(numberOfRows+1):
        for j in range(numberOfColumns+1):
            addClauses(vdc.zeroOrTwo(vdc.nodeWalls(i,j)))
    
    # One loop
    # @TODO
    

    normalizeClauses()
    return clauses

def CNFtoPicosat(program):
    def maximumVariable(program):
        return max([
                max([abs(x) for x in clause]) for clause in program
                   ])

    header = "p cnf {0} {1}".format(maximumVariable(program),len(program))
    
    body = "\n".join( 
                        [" ".join([str(x) for x in clause] + ["0"]) for clause in program]
                    )
    indata = header + "\n" + body + "\n"
    solver = subprocess.Popen(["picosat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    solver.stdin.write(indata.encode("utf-8"))
    outdata, errdata = solver.communicate()
    return outdata.decode("utf-8")

def visualize(rawOutput, rawInput):
    numberOfRows, numberOfColumns, grid = rawInput
    vdc = VDC(rawInput)

    activeWallss =  [ [ int(x) for x in  [x for x in line.split(" ")][1:] if int(x) > 0] for line in rawOutput.split("\n")[1:-1]]
    activeWalls = []
    for xs in activeWallss:
        for x in xs:
            activeWalls.append(x)
            
    for i in range(numberOfRows+1):
        print("+".join([""] + [{True:"-", False:" "}[vdc.wall(i,j,1) in activeWalls] for j in range(numberOfColumns)] + [""]))
        if i == numberOfRows: break
        print("".join([ {True:"|", False:" "}[vdc.wall(i,j,0) in activeWalls] + {True:str(grid[i][j]), False:" "}[grid[i][j] != -1] for j in range(numberOfColumns)]) +\
            {True:"|", False:" "}[vdc.wall(i,numberOfColumns,0) in activeWalls]) 

def main():
    rawInput = readTaskFromInput()
    program = rawInputToCNF(rawInput)
    print("CNF length: ", len(program))
    rawOutput = CNFtoPicosat(program)
    visualize(rawOutput, rawInput)

if __name__ == "__main__": main()
