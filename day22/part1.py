from os import lseek, replace
import re

def solution(filename):
    with open(filename) as fp:
        steps = fp.read().splitlines()

    reactor = [[[0] * 101 for _ in range(101)] for _ in range(101)]

    for step in steps:
        ranges = re.match('^(\w+) x=(-*\d+)\.\.(-*\d+),y=(-*\d+)\.\.(-*\d+),z=(-*\d+)\.\.(-*\d+)', step)
        command = ranges.group(1)
        x0 = int(ranges.group(2))
        x1 = int(ranges.group(3))
        y0 = int(ranges.group(4))
        y1 = int(ranges.group(5))
        z0 = int(ranges.group(6))
        z1 = int(ranges.group(7))

        if not -50 <= x0 <= 50:
            continue

        for i in range(x0, x1 + 1):
            for j in range(y0, y1 + 1):
                for k in range(z0, z1 + 1):
                    if command == 'on':
                        reactor[i + 50][j + 50][k + 50] = 1
                    else:
                        reactor[i + 50][j + 50][k + 50] = 0

    return sum([sum(row) for plane in reactor for row in plane])

if __name__ == "__main__":
    result = solution("./data/example1.txt")
    print(result)   # it should 39

    result = solution("./data/example2.txt")
    print(result)   # it should 590784

    result = solution("./data/input.txt")
    print(result)
