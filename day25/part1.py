from typing import List

EASTERN = '>'
SOUTHERN = 'v'
EMPTY = '.'

def parse_file(filename: str) -> List[List]:
    with open(filename) as fp:
        data = fp.read()

    sea_floor = []
    for line in data.splitlines():
        sea_floor.append([char for char in line])

    return sea_floor


def create_floor_for_easterns(sea_floor: List[List], rows: int, cols: int) -> List[List]:
    new_sea_floor = []
    for i, row in enumerate(sea_floor):
        new_row = []
        for j, location in enumerate(row):
            if location == SOUTHERN:
                new_row.append(SOUTHERN)
            else:
                new_row.append(EMPTY)
        new_sea_floor.append(new_row)

    return new_sea_floor


def create_floor_for_southerns(sea_floor: List[List], rows: int, cols: int) -> List[List]:
    new_sea_floor = []
    for i, row in enumerate(sea_floor):
        new_row = []
        for j, location in enumerate(row):
            if location == EASTERN:
                new_row.append(EASTERN)
            else:
                new_row.append(EMPTY)
        new_sea_floor.append(new_row)

    return new_sea_floor


def print_floor(floor: List[List]) -> None:
    for line in floor:
        print(''.join(line))
    print()

def solution(filename: str) -> int:
    sea_floor = parse_file(filename)
    sea_rows = len(sea_floor)
    sea_cols = len(sea_floor[0])

    step = 0
    while True:
        new_sea_floor = create_floor_for_easterns(sea_floor, sea_rows, sea_cols)
        movement = False

        # easterns
        for i, row in enumerate(sea_floor):
            for j, location in enumerate(row):
                if location == EASTERN:
                    next_j = (j + 1) % sea_cols
                    if sea_floor[i][next_j] == EMPTY:
                        new_sea_floor[i][next_j] = EASTERN
                        movement = True
                    else:
                        new_sea_floor[i][j] = EASTERN

        sea_floor = new_sea_floor
        new_sea_floor = create_floor_for_southerns(sea_floor, sea_rows, sea_cols)

        # southerns
        for i, row in enumerate(sea_floor):
            for j, location in enumerate(row):
                if location == SOUTHERN:
                    next_i = (i + 1) % sea_rows
                    if sea_floor[next_i][j] == EMPTY:
                        new_sea_floor[next_i][j] = SOUTHERN
                        movement = True
                    else:
                        new_sea_floor[i][j] = SOUTHERN

        step += 1
        if movement is False:
            break

        sea_floor = new_sea_floor

    return step

if __name__ == "__main__":
    # result = solution("./data/example1.txt")
    # print(result)

    # result = solution("./data/example2.txt")
    # print(result)

    # result = solution("./data/example3.txt")
    # print(result)

    result = solution("./data/input.txt")
    print(result)
