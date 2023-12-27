#!/usr/bin/python3

import sys

def isDigit(ch):
    return ch.isdigit()

def parse(line):
    digits = list(filter(isDigit, (c for c in line)))
    if len(digits) == 0:
        return 0
    first = digits[0]
    last = digits[-1]
    return int(first + last)

def main(inputfile):
    with open(inputfile, 'r', encoding='UTF-8') as file:
        result = sum(parse(line) for line in file)
        print(result)

if __name__ == '__main__':
    main(sys.argv[1])