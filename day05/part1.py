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
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                vent_diagram[x1][y] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                vent_diagram[x][y1] += 1

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
