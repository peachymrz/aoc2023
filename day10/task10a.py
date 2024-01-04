#!/usr/bin/python3

import sys

class PipeMap:
    directions = {
        ('|', 's') : 'n', # if current symbol is '|' and was entered from south, go to north
        ('|', 'n') : 's',
        ('-', 'w') : 'e',
        ('-', 'e') : 'w',
        ('L', 'n') : 'e',
        ('L', 'e') : 'n',
        ('J', 'n') : 'w',
        ('J', 'w') : 'n',
        ('F', 's') : 'e',
        ('F', 'e') : 's',
        ('7', 's') : 'w',
        ('7', 'w') : 's',
    }

    def __init__(self, map):
        self.map = map # list of strings
        self.currentPos = self.findStart()
        self.steps = 0
        

    def _isValidPos(self, pos):
        (x, y) = pos
        return y >= 0 and y < len(self.map) and x >= 0 and x < len(self.map[y])

    def findStart(self):
        for lineNo, line in enumerate(self.map):
            xPos = line.find('S')
            if xPos >= 0:
                return (xPos, lineNo)
        return None

    def goNorth(self):
        """
        check if going north is possible
        if yes, update position and return symbol of new position
        else do nothing and return None
        """
        (x, y) = self.currentPos
        if y == 0 or x >= len(self.map[y - 1]):
            # north of current pos is outside map
            return None
        symbol = self.map[y - 1][x]
        if symbol in 'LJ-.':
            # can't go north to these symbols
            return None
        self.currentPos = (x, y - 1)
        return symbol

    def goSouth(self):
        """
        check if going south is possible
        if yes, update position and return symbol of new position
        else do nothing and return None
        """
        (x, y) = self.currentPos
        if y == len(self.map) - 1 or x >= len(self.map[y + 1]):
            # south of current pos is outside map
            return None
        symbol = self.map[y + 1][x]
        if symbol in 'F7-.':
            # can't go south to these symbols
            return None
        self.currentPos = (x, y + 1)
        return symbol

    def goWest(self):
        """
        check if going west is possible
        if yes, update position and return symbol of new position
        else do nothing and return None
        """
        (x, y) = self.currentPos
        if x == 0:
            # west of current pos is outside map
            return None
        symbol = self.map[y][x - 1]
        if symbol in 'J7|.':
            # can't go west to these symbols
            return None
        self.currentPos = (x - 1, y)
        return symbol

    def goEast(self):
        """
        check if going east is possible
        if yes, update position and return symbol of new position
        else do nothing and return None
        """
        (x, y) = self.currentPos
        if x == len(self.map[y]) - 1:
            # east of current pos is outside map
            return None
        symbol = self.map[y][x + 1]
        if symbol in 'FL|.':
            # can't go east to these symbols
            return None
        self.currentPos = (x + 1, y)
        return symbol

    def _followPath(self, symbol, origin):
        while symbol is not None and symbol != 'S':
            dir = PipeMap.directions[(symbol, origin)]
            if dir == 'n':
                symbol = self.goNorth()
                origin = 's'
            elif dir == 's':
                symbol = self.goSouth()
                origin = 'n'
            elif dir == 'e':
                symbol = self.goEast()
                origin = 'w'
            elif dir == 'w':
                symbol = self.goWest()
                origin = 'e'
            self.steps += 1
        return symbol

    def findPath(self):
        self.currentPos = self.findStart()
        self.steps = 1
        symbol = self._followPath(self.goEast(), 'w')
        if symbol == 'S':
            return self.steps

        self.currentPos = self.findStart()
        self.steps = 1
        symbol = self._followPath(self.goSouth(), 'n')
        if symbol == 'S':
            return self.steps

        self.currentPos = self.findStart()
        self.steps = 1
        symbol = self._followPath(self.goWest(), 'e')
        if symbol == 'S':
            return self.steps

        return None


def main(inputfile):
    with open(inputfile, 'r', encoding='UTF-8') as file:
        lines = [line.rstrip() for line in file]
    pipeMap = PipeMap(lines)
    steps = pipeMap.findPath()
    print(f'steps = {steps}, half = {steps / 2}')


if __name__ == '__main__':
    main(sys.argv[1])