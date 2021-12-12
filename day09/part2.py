def get_neighbors_coords(i, j, heightmap, nrows, ncols):
    steps = [
        (0, -1),
        (0, 1),
        (-1, 0),
        (1, 0),
    ]
    neighbors_coords = []
    for row_step, col_step in steps:
        if (0 <= i + row_step < nrows) and (0 <= j + col_step < ncols):
            neighbors_coords.append((i + row_step, j + col_step))
    return neighbors_coords


def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()

    heightmap = [list(map(int,line)) for line in data]
    nrows = len(heightmap)
    ncols = len(heightmap[0])

    # determine low points
    low_points = []
    for i, row in enumerate(heightmap):
        for j, location in enumerate(row):
            neighbors = get_neighbors_coords(i, j, heightmap, nrows, ncols)
            for ni, nj in neighbors:
                neighbor = heightmap[ni][nj]
                if location >= neighbor:
                    break
            else:
                low_points.append((i, j))

    # traverse each low point and get all locations of a basin
    basins = []
    for i, j in low_points:
        basin = [(i, j)]

        # BFS
        visited = set()
        visited.add((i, j))
        queue = [(i, j)]
        while queue:
            li, lj = queue.pop(0)
            location = heightmap[li][lj]

            # traverse neighbors
            neighbors = get_neighbors_coords(li, lj, heightmap, nrows, ncols)
            for ni, nj in neighbors:
                neighbor = heightmap[ni][nj]
                if (ni, nj) not in visited:
                    if neighbor > location and neighbor != 9:
                        visited.add((ni, nj))
                        basin.append((ni, nj))
                        queue.append((ni, nj))

        basins.append(len(basin))

    basins.sort()
    return basins[-1] * basins[-2] * basins[-3]

if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 1134

    result = solution("./input.txt")
    print(result)
