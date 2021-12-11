def get_neighbors(i, j, heightmap, nrows, ncols):
    steps = [
        (0, -1),
        (0, 1),
        (-1, 0),
        (1, 0),
    ]
    neighbors_locations = []
    for row_step, col_step in steps:
        if (0 <= i + row_step < nrows) and (0 <= j + col_step < ncols):
            neighbors_locations.append(heightmap[i + row_step][j + col_step])
    return neighbors_locations


def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()

    heightmap = [list(line) for line in data]
    nrows = len(heightmap)
    ncols = len(heightmap[0])

    risk_level = 0
    for i, row in enumerate(heightmap):
        for j, location in enumerate(row):
            neighbors = get_neighbors(i, j, heightmap, nrows, ncols)
            for neighbor in neighbors:
                if location >= neighbor:
                    break
            else:
                risk_level += int(location) + 1

    return risk_level

if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 15

    result = solution("./input.txt")
    print(result)
