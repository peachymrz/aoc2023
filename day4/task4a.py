#!/usr/bin/python3

import re
import sys

RE_GAME = re.compile('^.*:(.*)\|(.*)$')

def numCardToIntList(numCard):
    return [int(n) for n in numCard.split()]

def countPoints(winNums, myNums):
    pts = 0
    for n in myNums:
        if n in winNums:
            pts = 1 if pts == 0 else pts * 2
    return pts

def pointsInLine(line):
    match = RE_GAME.match(line.strip())
    if match:
        winningCard = match.group(1)
        myCard = match.group(2)
        winningNums = numCardToIntList(winningCard)
        myNums = numCardToIntList(myCard)
        return countPoints(winningNums, myNums)
    return 0

def main(inputfile):
    with open(inputfile, 'r', encoding='UTF-8') as file:
        result = sum(pointsInLine(line) for line in file)
        print(f"result = {result}")
            

if __name__ == '__main__':
    main(sys.argv[1])