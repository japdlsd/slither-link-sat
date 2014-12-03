#!/usr/bin/python3

import itertools
import subprocess

def readTaskFromInput():
    numberOfRows, numberOfColumns = [int(x) for x in input().split(" ")]
    grid = [ [int(x) for x in input().split(" ")] for i in range(numberOfRows)]
    return (numberOfRows, numberOfColumns, grid)


class vdc:
    numberOfColumns=None
    numberOfRows=None
    grid=None

    def __init__(self, numberOfRows, numberOfColumns):
        pass

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

    def wallIsInRange(row, column, orientation):
        nonlocal numberOfRows
        nonlocal numberOfColumns
        if row < 0 or column < 0: return False
        if row > numberOfRows or column > numberOfColumns: return False
        if orientation == 0 and row == numberOfRows: return False
        if orientation == 1 and column == numberOfColumns: return False
        return True

    amountOfVerticalWalls = (numberOfColumns + 1) * numberOfRows
    amountOfHorizontalWalls = (numberOfRows + 1) * numberOfColumns
    def wall(row, column, orientation):
        """ `orientation` 0 - vertical, 1 - horizontal
        """
        assert(orientation in (0,1))
        assert(wallIsInRange(row, column, orientation))
        if orientation == 0: return 1 + column * numberOfRows + row
        if orientation == 1: return 1 + amountOfVerticalWalls + row * numberOfColumns + column
    
    def vTrue():
        return 1 + amountOfVerticalWalls + amountOfHorizontalWalls

    def vFalse():
        return -vTrue()

    def rcoFromWall(w):
        w -= 1
        assert(w < amountOfVerticalWalls + amountOfHorizontalWalls)
        if w < amountOfVerticalWalls:
            orientation = 0
            column, row = w // numberOfRows, w % numberOfRows
            return (row, column, orientation)
        else:
            w = w - amountOfVerticalWalls
            orientation = 1
            row, column = w // numberOfColumns, w % numberOfColumns
            return (row, column, orientation)

    def cellWalls(row, column):
        return [wall(row, column, 0), wall(row, column, 1), wall(row+1, column, 1), wall(row, column+1, 0)]
    
    def nodeWalls(row, column):
        possibleWalls = [(row, column, 0), (row, column, 1), (row-1, column, 0), (row, column-1, 1)]
        res = [wall(*w) for w in possibleWalls if wallIsInRange(*w)]
        assert(len(res) >= 2)
        return res

    def atMostN(vs, n):
        # at least one from n+1 variables are false
        return [[-c for c in cs] for cs in itertools.combinations(vs, n+1)]

    def atLeastN(vs, n):
        # at most N - n variables are false
        # so at least one from N - n + 1 is true
        return [list(cs) for cs in itertools.combinations(vs, len(vs) - n + 1)]

    def exactlyN(vs, n):
        return atMostN(vs, n) + atLeastN(vs, n)
    
    def zeroOrTwo(vs):
        """Full CNF computation.
        """ 
        res = []
        for cs in itertools.product(range(2), repeat=len(vs)):
            if sum(cs) not in (0, 2):
                res.append([(-1)**c * v for (c, v) in zip(cs, vs)])
        return res

    # Number of walls
    for i in range(numberOfRows):
        for j in range(numberOfColumns):
            if grid[i][j] != -1: 
                addClauses(exactlyN(cellWalls(i,j), grid[i][j]))
    
    # Connectivity
    for i in range(numberOfRows+1):
        for j in range(numberOfColumns+1):
            addClauses(zeroOrTwo(nodeWalls(i,j)))
    
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
    
    print("The calculaton has ended.")
    return outdata.decode("utf-8")

def visualize(rawOutput, rawInput):
    numberOfRows, numberOfColumns, grid = rawInput
    amountOfVerticalWalls = (numberOfColumns + 1) * numberOfRows
    amountOfHorizontalWalls = (numberOfRows + 1) * numberOfColumns
    def wallIsInRange(row, column, orientation):
        nonlocal numberOfRows
        nonlocal numberOfColumns
        if row < 0 or column < 0: return False
        if row > numberOfRows or column > numberOfColumns: return False
        if orientation == 0 and row == numberOfRows: return False
        if orientation == 1 and column == numberOfColumns: return False
        return True
    
    def wall(row, column, orientation):
        """ `orientation` 0 - vertical, 1 - horizontal
        """
        assert(orientation in (0,1))
        assert(wallIsInRange(row, column, orientation))
        if orientation == 0: return 1 + column * numberOfRows + row
        if orientation == 1: return 1 + amountOfVerticalWalls + row * numberOfColumns + column
    
    def rcoFromWall(w):
        w -= 1
        assert(w < amountOfVerticalWalls + amountOfHorizontalWalls)
        if w < amountOfVerticalWalls:
            orientation = 0
            column, row = w // numberOfRows, w % numberOfRows
            return (row, column, orientation)
        else:
            w = w - amountOfVerticalWalls
            orientation = 1
            row, column = w // numberOfColumns, w % numberOfColumns
            return (row, column, orientation)
    activeWallss =  [ [ int(x) for x in  [x for x in line.split(" ")][1:] if int(x) > 0] for line in rawOutput.split("\n")[1:-1]]
    activeWalls = []
    for xs in activeWallss:
        for x in xs:
            activeWalls.append(x)
            
    print("activeWalls= ", activeWalls)

    for i in range(numberOfRows+1):
        print("+".join([""] + [{True:"-", False:" "}[wall(i,j,1) in activeWalls] for j in range(numberOfColumns)] + [""]))
        if i == numberOfRows: break
        print("".join([ {True:"|", False:" "}[wall(i,j,0) in activeWalls] + {True:str(grid[i][j]), False:" "}[grid[i][j] != -1] for j in range(numberOfColumns)]) +\
            {True:"|", False:" "}[wall(i,numberOfColumns,0) in activeWalls]) 

def main():
    rawInput = readTaskFromInput()
    print(rawInput)
    program = rawInputToCNF(rawInput)
    print(program)
    rawOutput = CNFtoPicosat(program)
    print(rawOutput)
    visualize(rawOutput, rawInput)

if __name__ == "__main__": main()
