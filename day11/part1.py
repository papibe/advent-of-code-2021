def increase_neighbors_energy(i, j, octopuses, nrows, ncols):
    steps = [
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1)
    ]
    for row_step, col_step in steps:
        if (0 <= i + row_step < nrows) and (0 <= j + col_step < ncols):
            octopuses[i + row_step][j + col_step] += 1


def solution(filename, steps):
    with open(filename) as fp:
        data = fp.read().splitlines()

    octopuses = [list(map(int,line)) for line in data]
    nrows = len(octopuses)
    ncols = len(octopuses[0])

    total_flashes = 0
    for step in range(steps):
        # increase energy for all octopuses
        for i in range(nrows):
            for j in range(ncols):
                octopuses[i][j] += 1
        
        # check all flashes
        octopuses_flushed = set()
        while True:
            for i, row in enumerate(octopuses):
                for j, energy in enumerate(row):
                    if (i, j) not in octopuses_flushed and energy > 9:
                        octopuses_flushed.add((i, j))
                        increase_neighbors_energy(i, j, octopuses, nrows, ncols)
                        break
                else:
                    continue
                break
            else:
                # set energy to zero for flused octopuses
                for i, j in octopuses_flushed:
                    octopuses[i][j] = 0
                
                total_flashes += len(octopuses_flushed)
                break

    return total_flashes


if __name__ == "__main__":
    result = solution("./data/example1.txt", 2)
    print(result)   # it should be 9

    result = solution("./data/example2.txt", 100)
    print(result)   # it should be 1656


    result = solution("./data/input.txt", 100)
    print(result)
