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

def x_trayectory(velocity, step):
    if step < velocity + 1:
        return step * velocity - ((step - 1) * step) /2
    else:
        step = velocity + 1
        return step * velocity - ((step - 1) * step) /2


def solution(filename):
    with open(filename) as fp:
        data = fp.read()

    ranges = re.match('.*x=(\d+)\.\.(\d+).*y=(-*\d+)\.\.(-*\d+).*', data)
    x0 = int(ranges.group(1))
    x1 = int(ranges.group(2))
    y0 = int(ranges.group(3))
    y1 = int(ranges.group(4))

    velocities = 0
    for x_velocity in range(1000):
        for y_velocity in range(-1000, 1000):
            step1 = floor(quadratic(-0.5, y_velocity + 0.5, -y0))
            step0 = ceil(quadratic(-0.5, y_velocity + 0.5, -y1))

            for step in range(step0, step1 + 1):
                x = x_trayectory(x_velocity, step)
                y = step * y_velocity - ((step - 1) * step) /2
                if x0 <= x <= x1 and y0 <= y <= y1:
                    velocities += 1
                    break

    return velocities


if __name__ == "__main__":
    result = solution("./data/example.txt")
    print(result)   # it should be 45

    result = solution("./data/input.txt")
    print(result)
