import re

ON = 1
OFF = -1
CHANGE = -1
STATE = {'on': ON, 'off': OFF}


class Cuboid:

    def __init__(self, state, x0, y0, z0, x1, y1, z1) -> None:
        self.state = state
        self.min = [x0, y0, z0]
        self.max = [x1, y1, z1]

    def isOn(self):
        return self.state == ON
    
    def doesIntersects(self, cuboid):
        for i in range(3):
            if self.min[i] > cuboid.max[i] or self.max[i] < cuboid.min[i]:
                return False
        return True

    def intersection(self, cuboid, state):
        return Cuboid(
            state,
            max(self.min[0], cuboid.min[0]),
            max(self.min[1], cuboid.min[1]),
            max(self.min[2], cuboid.min[2]),

            min(self.max[0], cuboid.max[0]),
            min(self.max[1], cuboid.max[1]),
            min(self.max[2], cuboid.max[2]),
        )


    def volume(self):
        xdim = self.max[0] - self.min[0] + 1
        ydim = self.max[1] - self.min[1] + 1
        zdim = self.max[2] - self.min[2] + 1
        return xdim * ydim * zdim * self.state


def solution(filename):
    with open(filename) as fp:
        steps = fp.read().splitlines()
    
    reboot_steps = []
    for step in steps:
        ranges = re.match('^(\w+) x=(-*\d+)\.\.(-*\d+),y=(-*\d+)\.\.(-*\d+),z=(-*\d+)\.\.(-*\d+)', step)
        command = ranges.group(1)
        x0 = int(ranges.group(2))
        x1 = int(ranges.group(3))
        y0 = int(ranges.group(4))
        y1 = int(ranges.group(5))
        z0 = int(ranges.group(6))
        z1 = int(ranges.group(7))

        reboot_steps.append(Cuboid(STATE[command], x0, y0, z0, x1, y1, z1))

    visited = []
    intersections = []

    for cuboid in reboot_steps:
        new_intersections = []

        for vcuboid in visited:
            if cuboid.doesIntersects(vcuboid):
                new_intersections.append(cuboid.intersection(vcuboid, OFF))

        for cintersect in intersections:
            if cuboid.doesIntersects(cintersect):
                new_intersections.append(
                    cuboid.intersection(cintersect, cintersect.state * CHANGE)
                )

        if cuboid.isOn():
            visited.append(cuboid)

        intersections.extend(new_intersections)

    volume = sum([c.volume() for c in visited]) + \
        sum([c.volume() for c in intersections])

    return volume


if __name__ == "__main__":
    result = solution("./data/example3.txt")
    print(result)   # should be 2758514936282235

    result = solution("./data/input.txt")
    print(result)
