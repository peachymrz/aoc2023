#!/usr/bin/python3

import sys

matrix = []

def isSymbol(lidx, cidx):
    line = matrix[lidx]
    linelen = len(line)
    return cidx >= 0 and cidx < linelen and line[cidx] not in ".0123456789"

def hasSymbol(lidx, pos, numlen):
    if lidx < 0 or lidx >= len(matrix):
        return False
    for cidx in range(pos - 1, pos + numlen + 1):
        if isSymbol(lidx, cidx):
            return True
    return False

def getPartNumbers(lidx, numCoords):
    result = []
    for (pos, len) in numCoords:
        front = isSymbol(lidx, pos - 1)
        tail = isSymbol(lidx, pos + len)
        above = hasSymbol(lidx - 1, pos, len)
        below = hasSymbol(lidx + 1, pos, len)
        if front or tail or above or below:
            line = matrix[lidx]
            result.append(int(line[pos:pos+len]))
    return result


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

def evalMatrix():
    lineCount = len(matrix)
    result = 0
    for lidx in range(lineCount):
        numCoords = findNums(matrix[lidx])
        nums = getPartNumbers(lidx, numCoords)
        result += sum(nums)
    return result

def main(inputfile):
    with open(inputfile, 'r', encoding='UTF-8') as file:
        for line in file:
            matrix.append(line.strip())
    result = evalMatrix()
    print(f"result = {result}")
            

if __name__ == '__main__':
    main(sys.argv[1])