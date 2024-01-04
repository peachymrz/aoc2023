#!/usr/bin/python3

import sys
import re

class NodePath:
    def __init__(self, startNode):
        self.startNode = startNode

    def findLoop(self):
        pass


class NodeMap:
    def __init__(self, rl):
        self.rlInstructions = rl
        self.map = {}

    def add(self, curr, left, right):
        self.map[curr] = (left, right)

    def findStartPoints(self):
        return [key for key in self.map.keys() if key.endswith('A')]

    def getNext(self, curr, rlPos):
        nextDir = self.rlInstructions[rlPos]
        if nextDir == 'L':
            return self.map[curr][0]
        else:
            return self.map[curr][1]

    def findLoop(self, startNode):
        steps = 0
        rlLen = len(self.rlInstructions)
        currentNode = startNode
        seen = {} # key = node, val = steps
        endSteps = []
        while True:
            rlPos = steps % rlLen
            if rlPos == 0:
                if currentNode in seen:
                    startSteps = seen[currentNode]
                    return {
                        'startNode': startNode,  # node where this path started ('**A')
                        'loopNode': currentNode, # node where the loop starts
                        'startSteps': startSteps, # number of steps where the loop starts
                        'loopLen': steps - startSteps, # number of steps in a loop
                        'endSteps': endSteps     # list of nodes that are destinations ('**Z')
                    }
                else:
                    seen[currentNode] = steps
            if currentNode.endswith('Z'):
                endSteps.append(steps)
            currentNode = self.getNext(currentNode, rlPos)
            steps += 1

    def findPathWithMaxSteps(self, pathList):
        maxVal = 0
        for p in pathList:
            val = p['endSteps'][0]
            if val > maxVal:
                maxVal = val
        return maxVal

    def updateEndSteps(self, pathList, maxSteps):
        for p in pathList:
            while p['endSteps'][0] < maxSteps:
                step = p['endSteps'].pop(0)
                if step >= p['startSteps']:
                    p['endSteps'].append(step + p['loopLen'])

    def checkEndSteps(self, pathList):
        expect = pathList[0]['endSteps'][0]

        for p in pathList:
            val = p['endSteps'][0]
            if val != expect:
                return False
        return True

    def findAllPaths(self, pathList):
        while not self.checkEndSteps(pathList):
            maxStep = self.findPathWithMaxSteps(pathList)
            self.updateEndSteps(pathList, maxStep)
        return pathList[0]['endSteps'][0]


def main(inputfile):
    rlRegex = re.compile('^[RL]+$')
    dirRegex = re.compile('^([A-Z0-9]*) = \(([A-Z0-9]*), ([A-Z0-9]*)\)$')
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
    startNodes = nodeMap.findStartPoints()
    pathList = [nodeMap.findLoop(n) for n in startNodes]
    for p in pathList:
        print(f'loop for {p}')
    steps = nodeMap.findAllPaths(pathList)
    print(f'steps = {steps}')
            


if __name__ == '__main__':
    main(sys.argv[1])