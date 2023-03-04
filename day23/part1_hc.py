import heapq as hq

SPACE = "."
AISLE = 1

pocket_place: dict = {"A": 3, "B": 5, "C": 7, "D": 9}
pocket_colums: list = [3, 5, 7, 9]
pocket_lower_row: int = 2
pocket_upper_row: int = 3

energy_per_step = {"A": 1, "B": 10, "C": 100, "D": 1000}

final_position: dict = {
    (2, 3): "A",
    (3, 3): "A",
    (2, 5): "B",
    (3, 5): "B",
    (2, 7): "C",
    (3, 7): "C",
    (2, 9): "D",
    (3, 9): "D",
}


def get_next_moves(state: dict, position: list, burrow: list):
    next_moves = []
    current_row, current_col = position
    steps = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    burrow_rows = len(burrow)
    burrow_cols = len(burrow[0])
    for row_step, col_step in steps:
        if (
            0 <= (current_row + row_step) < burrow_rows
            and 0 <= (current_col + col_step) < burrow_cols
            and burrow[current_row + row_step][current_col + col_step] == SPACE
            and (current_row + row_step, current_col + col_step) not in state
        ):
            next_moves.append((current_row + row_step, current_col + col_step))

    return next_moves


def get_destinations(
    state: dict, amphipod: str, row: int, col: int, burrow: list
) -> list:
    destinations: dict = {}
    visited: set = set((row, col))
    queue: list = [(0, (row, col))]

    # BFS
    while queue:
        cost, position = queue.pop(0)
        next_moves = get_next_moves(state, position, burrow)
        for move in next_moves:
            if move not in visited:
                visited.add(move)
                destinations[move] = cost + energy_per_step[amphipod]
                queue.append((cost + energy_per_step[amphipod], move))
    return destinations


def add_new_move(moves: list, cost: int, curr: tuple, new: tuple, state: dict):
    new_state = state.copy()
    amphipod = new_state[curr]
    del new_state[curr]
    new_state[new] = amphipod

    moves.append((cost, new_state))


def get_moves(dict_state: dict, burrow: list) -> list:
    amphipods = dict_state
    moves = []
    for (row, col), amphipod in amphipods.items():
        if row == pocket_upper_row and col == pocket_place[amphipod]:
            continue
        if (
            row == pocket_lower_row
            and col == pocket_place[amphipod]
            and (pocket_upper_row, pocket_place[amphipod]) in amphipods
            and amphipods[(pocket_upper_row, pocket_place[amphipod])] == amphipod
        ):
            continue

        raw_moves = get_destinations(dict_state, amphipod, row, col, burrow)

        if row == AISLE:
            # can only move to a final destination
            if (pocket_upper_row, pocket_place[amphipod]) in raw_moves:
                cost = raw_moves[(pocket_upper_row, pocket_place[amphipod])]
                add_new_move(
                    moves, cost, (row, col), (pocket_upper_row, pocket_place[amphipod]), dict_state
                )
            elif (
                (pocket_lower_row, pocket_place[amphipod]) in raw_moves
                and (pocket_upper_row, pocket_place[amphipod]) in amphipods
                and amphipods[(pocket_upper_row, pocket_place[amphipod])] == amphipod
            ):
                cost = raw_moves[(pocket_lower_row, pocket_place[amphipod])]
                add_new_move(
                    moves, cost, (row, col), (pocket_lower_row, pocket_place[amphipod]), dict_state
                )
                cost = raw_moves[(pocket_lower_row, pocket_place[amphipod])]
            continue

        for move, cost in raw_moves.items():
            new_row, new_col = move

            # moving to aisle
            if new_row == AISLE and new_col in pocket_colums:
                continue
            if new_row in [pocket_lower_row, pocket_upper_row] and pocket_place[amphipod] != new_col:
                continue
            if new_row == pocket_lower_row and (pocket_upper_row, pocket_place[amphipod]) not in amphipods:
                continue
            if (
                new_row == pocket_lower_row
                and (pocket_upper_row, pocket_place[amphipod]) in amphipods
                and amphipods[(pocket_upper_row, pocket_place[amphipod])] != amphipod
            ):
                continue

            add_new_move(moves, cost, (row, col), move, dict_state)

    return moves


def print_burrow(state: dict, burrow: list) -> None:
    output = []
    for i, row in enumerate(burrow):
        for j, item in enumerate(row):
            if (i, j) in state:
                output.append(state[(i, j)])
            else:
                output.append(item)
        output.append("\n")
    print("".join(output))


def get_str_state(state: dict, burrow: list) -> str:
    str_state = []
    for i, row in enumerate(burrow):
        for j, cell in enumerate(row):
            if (i, j) in state:
                str_state.append(state[(i, j)])
            else:
                str_state.append(cell)

    return "".join(str_state)


def organize(dict_state, burrow, visited: set) -> bool:

    heap = []
    hq.heappush(heap, (0, id(dict_state), dict_state))
    visited = set()
    str_state = get_str_state(dict_state, burrow)
    # visited.add(str_state)

    cost_table = {str_state: 0}

    while heap:
        cost, _, state = hq.heappop(heap)

        current_str_state = get_str_state(state, burrow)

        if state == final_position:
            return cost

        for travel_cost, new_state in get_moves(state, burrow):

            str_state = get_str_state(new_state, burrow)
            if str_state in visited:
                continue

            old_cost = cost_table.get(str_state, float("inf"))
            new_cost = cost_table[current_str_state] + travel_cost

            if new_cost < old_cost:
                # visited.add(str_state)
                hq.heappush(heap, (new_cost, id(new_state), new_state))
                cost_table[str_state] = new_cost

        visited.add(current_str_state)

    return None


def solution(filename):
    with open(filename, "r") as fp:
        data = fp.read()

    dict_state = {}
    burrow = [list(line) for line in data.splitlines()]
    for i, row in enumerate(burrow):
        for j, cell in enumerate(row):
            if cell in "ABCD":
                dict_state[(i, j)] = cell
                burrow[i][j] = SPACE

    str_state = get_str_state(dict_state, burrow)
    visited = set()
    visited.add(str_state)

    result = organize(dict_state, burrow, visited)
    return result


if __name__ == "__main__":
    # result = solution("./data/acompleted.txt")
    # print(result)

    result = solution("./data/example1.txt")  # should be 12521
    print(result)

    result = solution("./data/input.txt")  # should be 18282
    print(result)
