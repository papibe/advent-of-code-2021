import re

def solution(filename):
    with open(filename) as fp:
        data = fp.read()

    ranges = re.match('.*y=(-*\d+)\.\.(-*\d+).*', data)
    y0 = int(ranges.group(1))
    y1 = int(ranges.group(2))

    total_max_altitude = 0
    for velocity in range(-2000, 2000):
        max_for_given_velocity = 0
        for step in range(500):
            y = step * velocity - ((step - 1) * step) /2
            max_for_given_velocity = max(y, max_for_given_velocity)
            if y0 <= y <= y1:
                total_max_altitude = max(max_for_given_velocity, total_max_altitude)

    return total_max_altitude


if __name__ == "__main__":
    result = solution("./data/example.txt")
    print(result)   # it should be 45

    result = solution("./data/input.txt")
    print(result)
