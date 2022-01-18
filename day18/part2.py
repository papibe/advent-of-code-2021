from json import loads
from copy import deepcopy

from part1 import TreeNode


def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()

    list_data = [loads(line) for line in data]

    snumbers = []
    for raw_snumber in list_data:
        snumbers.append(TreeNode.parse(raw_snumber))

    max_magnitude = float("-inf")
    for i, snumber1 in enumerate(snumbers):
        for j, snumber2 in enumerate(snumbers):
            if i == j:
                continue

            x = deepcopy(snumber1)
            y = deepcopy(snumber2)
            x.add(y)
            x.reduces()

            max_magnitude = max(x.magnitude(), max_magnitude)

    return max_magnitude


if __name__ == "__main__":
    result = solution("./data/input.txt")
    print(result)
