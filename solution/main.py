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
        self.amountOfWalls = self.amountOfHorizontalWalls + self.amountOfVerticalWalls
        self.maxTime = self.amountOfWalls

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
    
    def rcoFromWall(self, w):
        w -= 1
        assert(w < self.amountOfWalls)
        if w < self.amountOfVerticalWalls:
            orientation = 0
            column, row = w // self.numberOfRows, w % self.numberOfRows
            return (row, column, orientation)
        else:
            w = w - self.amountOfVerticalWalls
            orientation = 1
            row, column = w // self.numberOfColumns, w % self.numberOfColumns
            return (row, column, orientation)
    
    def reachable(self, row, column, orientation, time):
        assert(0 <= time <= self.maxTime)
        pref = self.amountOfWalls + 1
        return pref + time * self.amountOfWalls + self.wall(row, column, orientation) 

    def cellWalls(self, row, column):
        return [self.wall(row, column, 0), self.wall(row, column, 1), self.wall(row+1, column, 1), self.wall(row, column+1, 0)]
    
    def nodeWalls(self, row, column):
        possibleWalls = [(row, column, 0), (row, column, 1), (row-1, column, 0), (row, column-1, 1)]
        res = [self.wall(*w) for w in possibleWalls if self.wallIsInRange(*w)]
        assert(len(res) >= 2)
        return res
    
    def wallNeighbours(self, row, column, orientation):
        firstNode = (row, column)
        secondNode = {0:(row+1, column), 1:(row, column+1)}[orientation]
        return list(set( self.nodeWalls(*firstNode) + self.nodeWalls(*secondNode) ))
    
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
    
    def implies(self, A, B):
        """AND(A) -> OR(B) === OR(NOT Ai) OR OR(B)
        """
        return [[-x for x in A] + B]

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
    # everything except first wall is false at beginning
    # everything at end is equal to wall
    
    def findPositiveCell():
        for row in range(numberOfRows):
            for column in range(numberOfColumns):
                if grid[row][column] > 0:
                    return (row, column)
    positiveCell = findPositiveCell()
    rcoPossibleStarts = [vdc.rcoFromWall(w) for w in vdc.cellWalls(*positiveCell)]

    for i in range(len(rcoPossibleStarts)):
        # if previous walls are false and i-th is true, then its first wall
        prevWalls = rcoPossibleStarts[:i]
        addClauses(vdc.implies(
            [-vdc.wall(*x) for x in prevWalls] + [vdc.wall(*rcoPossibleStarts[i])],
            [vdc.reachable(*rcoPossibleStarts[i], time=0)]
        ))

        for otherWall in [x for x in rcoPossibleStarts if x != rcoPossibleStarts[i]]:
                addClauses(vdc.implies(
                    [-vdc.wall(*x) for x in prevWalls] + [vdc.wall(*rcoPossibleStarts[i])],
                    [-vdc.reachable(*otherWall, time=0)]
                ))
    for w in [vdc.rcoFromWall(w) for w in range(1, vdc.amountOfWalls + 1) if vdc.rcoFromWall(w) not in rcoPossibleStarts]:
        addClauses([[-vdc.reachable(*w, time=0)]])
    
    for w in [vdc.rcoFromWall(w) for w in range(1, vdc.amountOfWalls + 1)]:
        addClauses(vdc.implies(
            [vdc.reachable(*w, time=vdc.maxTime)],
            [vdc.wall(*w)]
        ))
        addClauses(vdc.implies(
            [vdc.wall(*w)],
            [vdc.reachable(*w, time=vdc.maxTime)]
        ))

    # inference rule:
    # if everything in neighbourhood at time t-1 is false, then I am false at time t
    # if not, then I am true at time t
    for t in range(1, vdc.maxTime+1):
        for w in [vdc.rcoFromWall(x) for x in range(1, vdc.amountOfWalls + 1)]:
            neighbourhood = [vdc.rcoFromWall(x) for x in vdc.wallNeighbours(*w)]
            # if w exitst
            addClauses(vdc.implies(
                [vdc.wall(*w)] + [-vdc.reachable(*x, time=t-1) for x in neighbourhood],
                [-vdc.reachable(*w, time=t)]
            ))
            for n in neighbourhood:
                addClauses(vdc.implies(
                    [vdc.wall(*w)] + [vdc.reachable(*n, time=t-1)],
                    [vdc.reachable(*w, time=t)]
                ))
            #if w doesn't exist
            addClauses(vdc.implies(
                [-vdc.wall(*w)],
                [-vdc.reachable(*w, time=t)]
            ))

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
    if "UNSATISFIABLE" in rawOutput:
        print("UNSATISFIABLE")
        #return

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

def visualizeDFS(rawOutput, rawInput):
    numberOfRows, numberOfColumns, grid = rawInput
    vdc = VDC(rawInput)
    if "UNSATISFIABLE" in rawOutput:
        print("UNSATISFIABLE")
        return

    activeVarss =  [ [ int(x) for x in  [x for x in line.split(" ")][1:] if int(x) > 0] for line in rawOutput.split("\n")[1:-1]]
    activeVars = []
    for xs in activeVarss:
        for x in xs:
            activeVars.append(x)
    
    activeWalls = [x for x in activeVars if x <= vdc.amountOfWalls]
    activeReachables = [x for x in activeVars if x > vdc.amountOfWalls]
    
    def isReached(row, column, orientation, time):
        nonlocal activeReachables
        return vdc.reachable(row, column, orientation, time) in activeReachables

    def rWall(row, column, orientation, time):
        return {(True, 0):"|", (False, 0):":", (True, 1):"-", (False, 1):"…"}[(isReached(row, column, orientation, time), orientation)]

    for t in range(0, vdc.maxTime//2):
        print ("time = " + str(t))
        for i in range(numberOfRows+1):
            print("+".join([""] + [{True:rWall(i, j, 1, t), False:" "}[vdc.wall(i,j,1) in activeWalls] for j in range(numberOfColumns)] + [""]))
            if i == numberOfRows: break
            print("".join([ {True:rWall(i,j,0,t), False:" "}[vdc.wall(i,j,0) in activeWalls] + {True:str(grid[i][j]), False:" "}[grid[i][j] != -1] for j in range(numberOfColumns)]) +\
                {True:rWall(i, numberOfColumns, 0, t), False:" "}[vdc.wall(i,numberOfColumns,0) in activeWalls]) 

def main():
    rawInput = readTaskFromInput()
    program = rawInputToCNF(rawInput)
    print("CNF length: ", len(program))
    rawOutput = CNFtoPicosat(program)
    visualize(rawOutput, rawInput)
    # visualizeDFS(rawOutput, rawInput)

if __name__ == "__main__": main()
