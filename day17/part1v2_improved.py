import re
from math import sqrt, floor, ceil


def quadratic(a, b, c):
    part1 = - b
    part2 = b**2 - (4 * a * c)
    if part2 >= 0:
        # return [part1 + sqrt(part2) / (2 * a), part1 - sqrt(part2) / (2 * a)]
        sol1 = (part1 + sqrt(part2)) / (2 * a)
        sol2 = (part1 - sqrt(part2)) / (2 * a)
        if sol1 > 0 and sol2 > 0:
            raise('confused')
        if sol1 >= 0:
            return sol1
        return sol2

    return None


def solution(filename):
    with open(filename) as fp:
        data = fp.read()

    ranges = re.match('.*y=(-*\d+)\.\.(-*\d+).*', data)
    y0 = int(ranges.group(1))
    y1 = int(ranges.group(2))

    total_max_altitude = 0
    for velocity in range(-2000, 2000):
        max_for_given_velocity = 0
        step1 = floor(quadratic(-0.5, velocity + 0.5, -y0))
        step0 = ceil(quadratic(-0.5, velocity + 0.5, -y1))

        for step in range(step0, step1 + 1):
            y = step * velocity - ((step - 1) * step) /2
            max_for_given_velocity = max(y, max_for_given_velocity)
            if y0 <= y <= y1:
                max_altitude_for_current_velocity = ((velocity + 0.5)** 2) / 2
                total_max_altitude = max(max_altitude_for_current_velocity, total_max_altitude)
                break

    return round(total_max_altitude)


if __name__ == "__main__":
    result = solution("./data/example.txt")
    print(result)   # it should be 45

    result = solution("./data/input.txt")
    print(result)
