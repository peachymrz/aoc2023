#!/usr/bin/python3

import re
import sys

class RangeMapper:
    def __init__(self, dst, src, len):
        self.source = src
        self.dest = dst
        self.rangeLen = len

    def inputInRange(self, input):
        return input >= self.source and input < self.source + self.rangeLen

    """
    returns a pair:
    1st value is mapped value
    2nd value is the number of values that are equal or greater than the for the input value
    and are still in this range
    or None if the input value is not in range
    example: src=3 len=7 dest=100 input=5 -> (102, ) 3 4 (5) 6 7 8 9
    """
    def map(self, input):
        mappedVal = self.dest + input - self.source
        remainRange = self.rangeLen - input + self.source
        return (mappedVal, remainRange) if self.inputInRange(input) else (input, None)

class RangeMapperList:
    def __init__(self):
        self.list = []

    def add(self, map):
        self.list.append(map)

    def map(self, input):
        firstSourceAfterInput = None
        for map in self.list:
            if map.source > input and (firstSourceAfterInput is None or firstSourceAfterInput > map.source):
                firstSourceAfterInput = map.source
            if map.inputInRange(input):
                return map.map(input)
        if firstSourceAfterInput is not None:
            firstSourceAfterInput -= input
        return (input, firstSourceAfterInput)

converters = [
    'seed-to-soil',
    'soil-to-fertilizer',
    'fertilizer-to-water',
    'water-to-light',
    'light-to-temperature',
    'temperature-to-humidity',
    'humidity-to-location'
]
rangeMappers = {}
RE_RANGE = re.compile('^([0-9]+) ([0-9]+) ([0-9]+)$')

def createRangeMapperFromLine(line):
    match = RE_RANGE.match(line.strip())
    if match:
        dst = int(match.group(1))
        src = int(match.group(2))
        len = int(match.group(3))
        return RangeMapper(dst, src, len)
    return None

def addRangeMapper(mapper, conv):
    if mapper is None or len(conv) == 0:
        return
    mapList = rangeMappers.get(conv)
    if mapList is None:
        mapList = RangeMapperList()
        rangeMappers[conv] = mapList
    mapList.add(mapper)

def updateRemainRange(minRemainRange, newRemainRange):
    if minRemainRange is None:
        return newRemainRange
    if newRemainRange is None:
        return minRemainRange
    return min(minRemainRange, newRemainRange)

def convertSeed(seed):
    minRemainRange = None
    for conv in converters:
        mapper = rangeMappers.get(conv)
        if mapper is not None:
            (seed, remainRange) = mapper.map(seed)
            minRemainRange = updateRemainRange(minRemainRange, remainRange)
    return (seed, minRemainRange)

def convertSeedRangeAndGetMin(startSeed, rangeLen):
    seed = startSeed
    endSeed = startSeed + rangeLen
    minConvertedSeed = None
    while seed < endSeed:
        (convertedSeed, minRemainRange) = convertSeed(seed)
        if minRemainRange is None:
            minRemainRange = 1
        seed += minRemainRange
        minConvertedSeed = convertedSeed if minConvertedSeed is None else min(convertedSeed, minConvertedSeed)
    return minConvertedSeed

def main(inputfile):
    activeConv = ''
    with open(inputfile, 'r', encoding='UTF-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('seeds:'):
                seeds = [int(seedTxt) for seedTxt in line[6:].strip().split()]
                continue
            if line.endswith(' map:'):
                conv = line[:-5]
                if conv in converters:
                    activeConv = conv
                continue
            mapper = createRangeMapperFromLine(line)
            addRangeMapper(mapper, activeConv)
    
    converted = []
    seedIter = iter(seeds)
    for (startSeed, rangeLen) in zip(seedIter, seedIter):
        print(f'converting {rangeLen} from {startSeed}')
        converted.append(convertSeedRangeAndGetMin(startSeed, rangeLen))

    print('converted:',converted)
    print('result:', min(converted))
            

if __name__ == '__main__':
    main(sys.argv[1])