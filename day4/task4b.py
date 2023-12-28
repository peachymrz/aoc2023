#!/usr/bin/python3

import re
import sys

RE_GAME = re.compile('^Card *([0-9]*):(.*)\|(.*)$')
wonCards = {} # key: card number, val: count

def numCardToIntList(numCard):
    return [int(n) for n in numCard.split()]

def countPoints(winNums, myNums):
    pts = 0
    for n in myNums:
        if n in winNums:
            pts += 1
    return pts

def addWonCardsAndGetCount(cardNum, addCount):
    currentCount = wonCards.get(cardNum, 0)
    currentCount += addCount
    wonCards[cardNum] = currentCount
    return currentCount

def pointsForLine(line):
    match = RE_GAME.match(line.strip())
    if match:
        cardNo = int(match.group(1))
        countForLine = addWonCardsAndGetCount(cardNo, 1)

        winningCard = match.group(2)
        myCard = match.group(3)
        winningNums = numCardToIntList(winningCard)
        myNums = numCardToIntList(myCard)
        winCount = countPoints(winningNums, myNums)
        for i in range(cardNo + 1, cardNo + 1 + winCount):
            addWonCardsAndGetCount(i, countForLine)
        return countForLine
    return 0

def main(inputfile):
    with open(inputfile, 'r', encoding='UTF-8') as file:
        result = sum(pointsForLine(line) for line in file)
        print(f"result = {result}")
            

if __name__ == '__main__':
    main(sys.argv[1])