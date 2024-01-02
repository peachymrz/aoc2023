#!/usr/bin/python3

import sys
import re

class NodeMap:
    def __init__(self, rl):
        self.rlInstructions = rl
        self.map = {}

    def add(self, curr, left, right):
        self.map[curr] = (left, right)

    def findPath(self):
        steps = 0
        rlPos = 0
        rlLen = len(self.rlInstructions)
        currentNode = 'AAA'
        while currentNode != 'ZZZ':
            steps += 1
            nextDir = self.rlInstructions[rlPos]
            if nextDir == 'L':
                currentNode = self.map[currentNode][0]
            else:
                currentNode = self.map[currentNode][1]
            rlPos = (rlPos + 1) % rlLen
        return steps


def main(inputfile):
    rlRegex = re.compile('^[RL]+$')
    dirRegex = re.compile('^([A-Z]*) = \(([A-Z]*), ([A-Z]*)\)$')
    with open(inputfile, 'r', encoding='UTF-8') as file:
        for line in file:
            line = line.strip()
            if rlRegex.match(line):
                nodeMap = NodeMap(line)
                continue
            match = dirRegex.match(line)
            if match:
                currentNode = match.group(1)
                leftNode = match.group(2)
                rightNode = match.group(3)
                nodeMap.add(currentNode, leftNode, rightNode)
    steps = nodeMap.findPath()
    print(f'steps = {steps}')
            


if __name__ == '__main__':
    main(sys.argv[1])