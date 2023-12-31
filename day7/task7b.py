#!/usr/bin/python3

import sys

class Hand:
    cardVal = {
        'J':0,
        '2':1, '3':2, '4':3, '5':4, '6':5, '7':6, '8':7, '9':8,
        'T':9, 'Q':10, 'K':11, 'A':12
        }

    def __init__(self, cards, bet):
        self.cards = cards
        self.bet = int(bet)
        self.value = self._eval(cards)
        

    def _eval(self, cards):
        cardCount = {}
        for c in cards:
            cnt = cardCount.get(c, 0) + 1
            cardCount[c] = cnt
        jokerCount = cardCount.pop('J', 0) # remember number of jokers
        valList = sorted(cardCount.values(), reverse = True)
        if len(valList) > 0:
            valList[0] += jokerCount  # add jokers to whatever is already the top count
        else:
            valList.append(jokerCount) # or just use the joker count as the only count
        while len(valList) < 5:
            valList.append(0)
        val = 0
        for d in valList:
            val = val * 10 + d
        return val

    def getValue(self):
        return self.value

    def getBet(self):
        return self.bet

    def __lt__(self, other):
        if self.value < other.value:
            return True
        if self.value > other.value:
            return False
        if self.value == other.value:
            for (a, b) in zip(self.cards, other.cards):
                a = Hand.cardVal[a]
                b = Hand.cardVal[b]
                if a < b:
                    return True
                if a > b:
                    return False
        return False

    def __str__(self):
        return self.cards

    def __repr__(self):
        return f'Hand({self.cards})'


def main(inputfile):
    handList = []
    with open(inputfile, 'r', encoding='UTF-8') as file:
        for line in file:
            h = Hand(*(line.split()))
            handList.append(h)

    handList.sort()
    totalWin = 0
    for idx, hand in enumerate(handList):
        totalWin += ((idx + 1) * hand.getBet())
    print(f'total win = {totalWin}')

if __name__ == '__main__':
    main(sys.argv[1])