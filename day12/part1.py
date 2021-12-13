def is_small_cave(cave):
    if cave.islower():
        return True
    return False


def connect(cave1, cave2, adjacency_dict):
    if cave1 in adjacency_dict:
        adjacency_dict[cave1].append(cave2)
    else:
        adjacency_dict[cave1] = [cave2]


def get_valid_paths(current, end, adjacency_dict, visited, path, solutions):
    if current == 'end':
        solutions.append(path)
        return

    for cave in adjacency_dict[current]:
        if cave in visited:
            continue

        if is_small_cave(cave):
            visited.add(cave)
        path.append(cave)
        get_valid_paths(cave, end, adjacency_dict, visited, path, solutions)
        path.pop()
        if is_small_cave(cave):
            visited.remove(cave)


def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()

    adjacency_dict = {}
    for line in data:
        cave1, cave2 = line.split('-')
        connect(cave1, cave2, adjacency_dict)
        connect(cave2, cave1, adjacency_dict)

    solutions = []
    path = ['start']
    visited = set()
    visited.add('start')
    get_valid_paths('start', 'end', adjacency_dict, visited, path, solutions)

    return len(solutions)


if __name__ == "__main__":
    result = solution("./data/example1.txt")
    print(result)   # it should be 10

    result = solution("./data/example2.txt")
    print(result)   # it should be 19

    result = solution("./data/example3.txt")
    print(result)   # it should be 226

    result = solution("./data/input.txt")
    print(result)
