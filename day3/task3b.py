#!/usr/bin/python3

import sys

matrix = []

def findNums(line):
    result = []
    pos = -1
    len = -1
    for cidx, c in enumerate(line):
        if c.isdigit():
            if pos < 0:
                pos = cidx
                len = 1
            else:
                len += 1
        else:
            if pos >= 0:
                result.append((pos, len))
            pos = -1
            len = -1
    # if a number is at end of line
    if pos >= 0:
        result.append((pos, len))
    return result

def findAdjacentNums(lidx, pos):
    adjacentNums = []
    if lidx >= 0 and lidx < len(matrix):
        line = matrix[lidx]
        numsInLine = findNums(line)
        for numPos, numLen in numsInLine:
            if pos >= numPos - 1 and pos <= numPos + numLen:
                adjacentNums.append(int(line[numPos:numPos+numLen]))
    return adjacentNums

def checkForGear(lidx, pos):
    adjacentNums = []
    adjacentNums.extend(findAdjacentNums(lidx - 1, pos))
    adjacentNums.extend(findAdjacentNums(lidx, pos))
    adjacentNums.extend(findAdjacentNums(lidx + 1, pos))
    return adjacentNums[0] * adjacentNums[1] if len(adjacentNums) == 2 else 0


def findGearsInLine(lidx):
    gears = []
    startPos = 0
    while True:
        pos = matrix[lidx].find('*', startPos)
        if pos < 0:
            break
        startPos = pos + 1
        gear = checkForGear(lidx, pos)
        if gear > 0:
            gears.append(gear)
    return gears


def evalMatrix():
    lineCount = len(matrix)
    result = 0
    for lidx in range(lineCount):
        gears = findGearsInLine(lidx)
        result += sum(gears)
    return result

def main(inputfile):
    with open(inputfile, 'r', encoding='UTF-8') as file:
        for line in file:
            matrix.append(line.strip())
    result = evalMatrix()
    print(f"result = {result}")
            

if __name__ == '__main__':
    main(sys.argv[1])