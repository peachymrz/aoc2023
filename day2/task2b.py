#!/usr/bin/python3

import re
import sys

RE_OBJ = re.compile('^Game ([0-9]*): (.*)$')
RE_SET = re.compile('^([0-9]*) *(.*)$')
GAME_BAG = {'red' : 12, 'green': 13, 'blue': 14}

def getPowerOfGame(gameLog):
    gameBag = {'red' : 0, 'green': 0, 'blue': 0}
    gameSets = gameLog.split(';')
    for gameSet in gameSets:
        colorAndNums = gameSet.split(',')
        for colAndNum in colorAndNums:
            match = RE_SET.match(colAndNum.strip())
            if match:
                num = int(match.group(1))
                color = match.group(2)
                if gameBag[color] < num:
                    gameBag[color] = num
    return gameBag['red'] * gameBag['green'] * gameBag['blue']

def parseLine(line):
    match = RE_OBJ.match(line.strip())
    if match:
        gameId = int(match.group(1))
        gameLog = match.group(2)
        return getPowerOfGame(gameLog)

def main(inputfile):
    with open(inputfile, 'r', encoding='UTF-8') as file:
        result = sum(parseLine(line) for line in file)
        print('result=', result)
            

if __name__ == '__main__':
    main(sys.argv[1])