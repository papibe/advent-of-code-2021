def calulate_step(c1, c2):
    diff = c2 - c1
    if diff == 0:
        return 0
    return 1 if diff > 0 else -1

def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()

    vent_coords = []
    values = []
    for line in data:
        raw_coords = line.split(' -> ')
        first_coords = list(map(int, raw_coords[0].split(',')))
        last_coords = list(map(int, raw_coords[1].split(',')))

        vent_coords.append([first_coords, last_coords])
        values.extend(first_coords + last_coords)

    # create vent diagram
    map_size = max(values) + 1
    vent_diagram = [[0] * map_size for _ in range(map_size)]

    for (x1, y1), (x2, y2) in vent_coords:
        startx = x1
        starty = y1
        dirx = calulate_step(x1, x2)
        diry = calulate_step(y1, y2)
        while startx != x2 or starty != y2:
            vent_diagram[startx][starty] += 1
            startx += dirx
            starty += diry

        vent_diagram[startx][starty] += 1

    # count most dangerous areas
    counter = 0
    for row in vent_diagram:
        for vent in row:
            if vent > 1:
                counter += 1

    return counter

if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 198

    result = solution("./input.txt")
    print(result)
