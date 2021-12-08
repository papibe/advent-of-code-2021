from functools import reduce
from math import sqrt, floor

def solution(filename):
    with open(filename) as fp:
        raw_data = fp.read()

    crab_positions = list(map(int, raw_data.split(',')))
    crab_positions.sort()
    length = len(crab_positions)

    if length % 2 == 0:
        median = crab_positions[floor(length // 2)]
    else:
        index = length // 2
        median = (crab_positions[index] - crab_positions[index -1]) // 2

    return sum(map(lambda x: abs(x - median), crab_positions))

if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 37

    result = solution("./input.txt")
    print(result)
