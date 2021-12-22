import re

def solution(filename):
    with open(filename) as fp:
        data = fp.read()

    ranges = re.match('.*x=(\d+)\.\.(\d+).*y=(-*\d+)\.\.(-*\d+).*', data)
    x0 = int(ranges.group(1))
    x1 = int(ranges.group(2))
    y0 = int(ranges.group(3))
    y1 = int(ranges.group(4))

    def x_trayectory(velocity, step):
        if step < velocity + 1:
            return step * velocity - ((step - 1) * step) /2
        else:
            step = velocity + 1
            return step * velocity - ((step - 1) * step) /2

    velocities = 0
    for x_velocity in range(1000):
        for y_velocity in range(-1000, 1000):
            for step in range(1000):
                x = x_trayectory(x_velocity, step)
                y = step * y_velocity - ((step - 1) * step) /2
                if x0 <= x <= x1 and y0 <= y <= y1:
                    velocities += 1
                    print(velocities)
                    break

    return velocities


if __name__ == "__main__":
    # result = solution("./data/example.txt")
    # print(result)   # it should be 45

    result = solution("./data/input.txt")
    print(result)
