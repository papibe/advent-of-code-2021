def is_small_cave(cave):
    if cave.islower():
        return True
    return False


def connect(cave1, cave2, adjacency_dict):
    if cave1 in adjacency_dict:
        adjacency_dict[cave1].append(cave2)
    else:
        adjacency_dict[cave1] = [cave2]


def possible_visit(visited, cave):
    if not is_small_cave(cave):
        return True

    if visited[cave] + 1 > 2:
        return False

    if (visited[cave] + 1 == 2) and visited['twice']:
        return False

    visited[cave] += 1
    if visited[cave] == 2:
        visited['twice'] = True
    return True


def remove_visited(visited, cave):
    if is_small_cave(cave):
        visited[cave] -= 1
        if visited[cave] == 1:
            visited['twice'] = False


def get_valid_paths(current, end, adjacency_dict, visited, path, solutions):
    if current == 'end':
        solutions.append(path)
        return

    for cave in adjacency_dict[current]:
        if not possible_visit(visited, cave):
            continue
        path.append(cave)
        get_valid_paths(cave, end, adjacency_dict, visited, path, solutions)
        path.pop()
        remove_visited(visited, cave)


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
    visited = {cave: 0 for cave in adjacency_dict if is_small_cave(cave)}
    visited['start'] = 2
    visited['twice'] = False
    get_valid_paths('start', 'end', adjacency_dict, visited, path, solutions)

    return len(solutions)


if __name__ == "__main__":
    result = solution("./data/example1.txt")
    print(result)   # it should be 36

    result = solution("./data/example2.txt")
    print(result)   # it should be 103

    result = solution("./data/example3.txt")
    print(result)   # it should be 3509

    result = solution("./data/input.txt")
    print(result)
