#!/usr/bin/python3

import sys
from functools import reduce

def distForRace(chargeTime, raceTime):
    speed = chargeTime # 1 mm/ms for each ms of charge time
    timeLeftToRace = raceTime - chargeTime
    return speed * timeLeftToRace

def findWinningStrategies(raceTime, minDist):
    # must charge at least one ms to have a speed > 0
    # must charge less than whole race time to have time left to race after charge
    winCount = 0
    for chargeTime in range(1, raceTime):
        dist = distForRace(chargeTime, raceTime)
        if dist > minDist:
            winCount += 1
    print(f'time: {raceTime},  dist: {minDist}, wins={winCount}')
    return  winCount


def main(inputfile):
    with open(inputfile, 'r', encoding='UTF-8') as file:
        for line in file:
            if line.startswith('Time:'):
                timeVal = int(line[5:].strip().replace(' ', ''))
            if line.startswith('Distance:'):
                distanceVal = int(line[9:].strip().replace(' ', ''))
    
    result = findWinningStrategies(timeVal, distanceVal)
    print(f'result: {result}')

if __name__ == '__main__':
    main(sys.argv[1])