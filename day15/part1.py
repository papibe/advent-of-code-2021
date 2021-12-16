from queue import PriorityQueue

current_lowest_risk = float('inf')

def get_neighbors_coords(i, j, heightmap):
    steps = [
        (0, -1),
        (0, 1),
        (-1, 0),
        (1, 0),
    ]
    nrows = len(heightmap)
    ncols = len(heightmap[0])
    neighbors_coords = []
    for row_step, col_step in steps:
        if (0 <= i + row_step < nrows) and (0 <= j + col_step < ncols):
            value = heightmap[i + row_step][j + col_step]
            neighbors_coords.append((i + row_step, j + col_step, value))
    return neighbors_coords


def risk_dijkstra(density_map):
    end = (len(density_map) - 1, len(density_map[0]) - 1)

    risks = {}
    for i in range(len(density_map)):
        for j in range(len(density_map[0])):
            risks[(i, j)] = float('inf')

    visited = set()
    risks[(0, 0)] = 0   # dijkstra's distances

    pqueue = PriorityQueue()
    pqueue.put((0, (0,0)))

    while not pqueue.empty():
        current_risk, (row, col) = pqueue.get()
        visited.add((row, col))

        for i, j, risk in get_neighbors_coords(row, col, density_map):
            if (i, j) not in visited:
                old_risk = risks[(i, j)]
                new_risk = risks[(row, col)] + risk
                if new_risk < old_risk:
                    pqueue.put((new_risk, (i, j)))
                    risks[(i, j)] = new_risk

    return risks[end]


def solution(filename):
    with open(filename) as fp:
        data = fp.read().split()

    density_map = [[int(n) for n in line] for line in data]
    return risk_dijkstra(density_map)


if __name__ == "__main__":
    result = solution("./data/example.txt")
    print(result)   # it should be 40

    result = solution("./data/input.txt")
    print(result)
