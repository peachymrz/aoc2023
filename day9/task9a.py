#!/usr/bin/python3

import sys

def allItemsZero(nums):
    for n in nums:
        if n != 0:
            return False
    return True

def makeDiff(nums):
    diffNums = []
    for i in range(1, len(nums)):
        diffNums.append(nums[i] - nums[i - 1])
    return diffNums

def extendNums(numSeq):
    # the rules require that the last number list has only 0
    numSeq[-1].append(0)
    for idx in range(len(numSeq) - 1, 0, -1):
        numSeq[idx - 1].append(numSeq[idx - 1][-1] + numSeq[idx][-1])
    return numSeq[0][-1]
    
def evalNums(nums):
    if len(nums) == 0:
        return 0
    seq = [nums]
    while not allItemsZero(seq[-1]):
        seq.append(makeDiff(seq[-1]))
    return extendNums(seq)
    
    

def main(inputfile):
    with open(inputfile, 'r', encoding='UTF-8') as file:
        sum = 0
        for line in file:
            nums = [int(nstr) for nstr in line.strip().split()]
            sum += evalNums(nums)
        print(f'sum = {sum}')
            

if __name__ == '__main__':
    main(sys.argv[1])