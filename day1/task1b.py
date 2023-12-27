#!/usr/bin/python3

import sys

textDigits = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

def findFirstDigit(line):
    minIdx = None
    digit = 0
    for i in range(0, 10):
        pos = line.find(str(i))
        if pos >= 0 and (minIdx is None or pos < minIdx):
            minIdx = pos
            digit = i

    for txt, num in textDigits.items():
        pos = line.find(txt)
        if pos >= 0 and (minIdx is None or pos < minIdx):
            minIdx = pos
            digit = num
    
    return digit

def findLastDigit(line):
    maxIdx = None
    digit = 0
    for i in range(0, 10):
        pos = line.rfind(str(i))
        if pos >= 0 and (maxIdx is None or pos > maxIdx):
            maxIdx = pos
            digit = i

    for txt, num in textDigits.items():
        pos = line.rfind(txt)
        if pos >= 0 and (maxIdx is None or pos > maxIdx):
            maxIdx = pos
            digit = num
    
    return digit

def parse(line):
    first = findFirstDigit(line)
    last = findLastDigit(line)
    return first * 10 + last

def main(inputfile):
    with open(inputfile, 'r', encoding='UTF-8') as file:
        result = sum(parse(line) for line in file)
        print(result)

if __name__ == '__main__':
    main(sys.argv[1])