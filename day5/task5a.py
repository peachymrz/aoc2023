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

    def map(self, input):
        return self.dest + input - self.source if self.inputInRange(input) else input

class RangeMapperList:
    def __init__(self):
        self.list = []

    def add(self, map):
        self.list.append(map)

    def map(self, input):
        for map in self.list:
            if map.inputInRange(input):
                return map.map(input)
        return input

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


def convertSeed(seed):
    for conv in converters:
        mapper = rangeMappers.get(conv)
        if mapper is not None:
            seed = mapper.map(seed)
    return seed

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
    
    converted = [convertSeed(s) for s in seeds]
    print('converted:',converted)
    print('result:', min(converted))
            

if __name__ == '__main__':
    main(sys.argv[1])