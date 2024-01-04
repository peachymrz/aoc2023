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
        self.foundMap = self._initEmptyMap()
        self.currentPos = self.findStart()
        self.steps = 0
        
    def _initEmptyMap(self):
        """
        creates an empty map (only '.') with the same dimension as the input
        """
        return [list('.'*len(l)) for l in self.map]

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

    def _markFoundSymbol(self, symbol):
        (x, y) = self.currentPos
        self.foundMap[y][x] = symbol

    def _followPath(self, symbol, origin):
        while symbol is not None and symbol != 'S':
            self._markFoundSymbol(symbol)
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
        return (symbol, origin)

    def _prepareRun(self):
        self.currentPos = self.findStart()
        self.steps = 1
        self.foundMap = self._initEmptyMap()

    def findPath(self):
        self._prepareRun()
        (symbol, origin) = self._followPath(self.goEast(), 'w')
        if symbol == 'S':
            if origin == 'n':
                self._markFoundSymbol('L')
            elif origin == 'w':
                self._markFoundSymbol('-')
            elif origin == 's':
                self._markFoundSymbol('F')
            return self.steps

        self._prepareRun()
        (symbol, origin) = self._followPath(self.goSouth(), 'n')
        if symbol == 'S':
            if origin == 'n':
                self._markFoundSymbol('|')
            elif origin == 'w':
                self._markFoundSymbol('7')
            elif origin == 'e':
                self._markFoundSymbol('F')
            return self.steps

        self._prepareRun()
        (symbol, origin) = self._followPath(self.goWest(), 'e')
        if symbol == 'S':
            if origin == 'n':
                self._markFoundSymbol('J')
            elif origin == 's':
                self._markFoundSymbol('7')
            elif origin == 'e':
                self._markFoundSymbol('-')
            return self.steps

        return None

    def countInside(self):
        count = 0
        for line in self.foundMap:
            inside = False
            corner = None
            for i, symbol in enumerate(line):
                if symbol == '|':
                    inside = not inside
                elif symbol in 'LF7J':
                    if corner is None:
                        corner = symbol
                    else:
                        if (corner in 'LJ' and symbol in 'F7') or (corner in 'F7' and symbol in 'LJ'):
                            inside = not inside
                        corner = None
                elif symbol == '.' and inside:
                    line[i] = 'I'
                    count += 1
            print(''.join(line))
        return count

def main(inputfile):
    with open(inputfile, 'r', encoding='UTF-8') as file:
        lines = [line.rstrip() for line in file]
    pipeMap = PipeMap(lines)
    steps = pipeMap.findPath()
    insideCount = pipeMap.countInside()
    print(f'steps = {steps}, half = {steps / 2}, inside = {insideCount}')


if __name__ == '__main__':
    main(sys.argv[1])