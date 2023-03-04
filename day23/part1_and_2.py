import heapq as hq
from collections import deque, defaultdict
from copy import deepcopy

SPACE = "."
AISLE = 1

allowed_aile_positions = {(1, 1), (1, 2), (1, 4), (1, 6), (1, 8), (1, 10), (1, 11)}

pocket_place: dict = {"A": 3, "B": 5, "C": 7, "D": 9}
pocket_colums: list = {3, 5, 7, 9}
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


class Amphipod:
    def __init__(self, kind, position) -> None:
        self.kind = kind
        self.position = position

    def set_position(self, new_position):
        self.position = new_position

    def __repr__(self) -> str:
        return f"{self.kind}{self.position}"


class Burrow:
    def __init__(self, rooms, amphipods, burrow_layout) -> None:
        self.rooms = rooms
        self.room_size = len(burrow_layout) - 3
        self.available = amphipods
        self.located = {}
        self.hallway = {}
        self.layout = burrow_layout

        for room_name in "ABCD":
            room_col = pocket_place[room_name]
            for row in range(len(self.layout) - 2, 1, -1):

                if self.available[(row, room_col)].kind != room_name:
                    break

                if self.available[(row, room_col)].kind == room_name:
                    self.located[(row, room_col)] = self.available[(row, room_col)]
                    del self.available[(row, room_col)]

    def is_room_clean(self, room_name) -> bool:
        room_col = pocket_place[room_name]
        for row in range(len(self.layout) - 2, 1, -1):
            assert self.layout[row][room_col] != "#"
            if (row, room_col) in self.located and self.located[
                (row, room_col)
            ].kind != room_name:
                return False
            if (row, room_col) in self.available and self.available[
                (row, room_col)
            ].kind != room_name:
                return False

        return True

    def insert(self, amphipod, room_name):
        self.room[room_name].apppend(amphipod)

    def is_organized(self):
        for room_name in "ABCD":
            room_col = pocket_place[room_name]
            for row in range(len(self.layout) - 2, 1, -1):
                assert self.layout[row][room_col] != "#"

                if (row, room_col) not in self.located:
                    return False
                if self.located[(row, room_col)].kind != room_name:
                    return False

        return True

    def get_str_state(self):
        str_state = []
        for i, row in enumerate(self.layout):
            for j, cell in enumerate(row):
                if (i, j) in self.available:
                    str_state.append(self.available[(i, j)].kind)
                elif (i, j) in self.located:
                    str_state.append(self.located[(i, j)].kind)
                elif (i, j) in self.hallway:
                    str_state.append(self.hallway[(i, j)].kind)
                else:
                    str_state.append(cell)
            str_state.append("\n")

        return "".join(str_state)

    def __lt__(self, other):
        return len(self.located) < len(other.located)
        # return len(self.located) > len(other.located)

    def __repr__(self) -> str:
        return (
            self.get_str_state()
            # + f"{self.available = }\n{self.located = }\n{self.hallway = }\n{self.rooms = }"
            + f"{self.available = }\n{self.located = }\n{self.hallway = }"
        )

    def check(self):
        return len(self.available) + len(self.located) + len(self.hallway) == 8


def parse(filename: str):
    with open(filename, "r") as fp:
        data = fp.read()

    burrow = [list(line) for line in data.splitlines()]
    available = {}
    rooms = defaultdict(list)

    row_number = len(burrow) - 1
    while row_number >= 0:
        row = burrow[row_number]
        for col_number, cell in enumerate(row):
            if cell in "ABCD":
                burrow[row_number][col_number] = SPACE

                amphipod = Amphipod(cell, (row_number, col_number))
                available[(row_number, col_number)] = amphipod
                rooms[col_number].append(amphipod)
        row_number -= 1

    return Burrow(rooms, available, burrow)


def get_next_moves(burrow, position, layout):
    next_moves = []
    current_row, current_col = position
    steps = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    burrow_rows = len(layout)
    burrow_cols = len(layout[0])
    for row_step, col_step in steps:
        if (
            # 0 <= (current_row + row_step) < burrow_rows
            # and 0 <= (current_col + col_step) < burrow_cols
            layout[current_row + row_step][current_col + col_step] == SPACE
            and (current_row + row_step, current_col + col_step) not in burrow.available
            and (current_row + row_step, current_col + col_step) not in burrow.hallway
            and (current_row + row_step, current_col + col_step) not in burrow.located
        ):
            next_moves.append((current_row + row_step, current_col + col_step))

    return next_moves


def get_destinations(burrow, amphipod):
    row, col = amphipod.position
    layout = burrow.layout
    destinations = []
    visited = set((row, col))
    queue = deque([(0, (row, col))])

    # BFS
    while queue:
        cost, position = queue.pop()
        next_moves = get_next_moves(burrow, position, layout)
        for move in next_moves:
            if move not in visited:
                visited.add(move)
                destinations.append((move, cost + energy_per_step[amphipod.kind]))
                queue.append((cost + energy_per_step[amphipod.kind], move))
    return destinations


def filter_hallway_positions(destinations):
    hallway_destinations = []
    other_destinations = []
    for move, cost in destinations:
        next_row, _ = move
        if next_row == AISLE:
            if move in allowed_aile_positions:
                hallway_destinations.append((move, cost))
        else:
            other_destinations.append((move, cost))
    return hallway_destinations, other_destinations


def filter_final_destination(burrow, destinations, amphipod):
    if not burrow.is_room_clean(amphipod.kind):
        return None

    lower_row = 0
    cost_at_lower_row = 0
    proper_destination_col = pocket_place[amphipod.kind]
    for move, cost in destinations:
        next_row, next_col = move
        if next_col == proper_destination_col:
            if next_row > lower_row:
                lower_row = next_row
                cost_at_lower_row = cost

    position = (lower_row, proper_destination_col)
    return None if lower_row == 0 else (position, cost_at_lower_row)

def is_top_stack(position, burrow):
    row, col = position
    if (row - 1, col) in burrow.available:
        return False
    return True

def get_next_states(burrow):
    moves = []
    for position, amphipod in burrow.hallway.items():
        destinations = get_destinations(burrow, amphipod)
        hallway_destinations, other_destinations = filter_hallway_positions(
            destinations
        )
        final_destination = filter_final_destination(
            burrow, other_destinations, amphipod
        )
        if final_destination:
            move, cost = final_destination

            new_burrow = deepcopy(burrow)
            new_amphipod = Amphipod(amphipod.kind, move)
            del new_burrow.hallway[position]

            new_burrow.located[move] = new_amphipod

            # print(new_burrow)
            moves.append((cost, new_burrow))

    for position, amphipod in burrow.available.items():
        if not is_top_stack(position, burrow):
            continue
        destinations = get_destinations(burrow, amphipod)
        hallway_destinations, other_destinations = filter_hallway_positions(
            destinations
        )
        final_destination = filter_final_destination(
            burrow, other_destinations, amphipod
        )
        if final_destination:
            move, cost = final_destination

            new_burrow = deepcopy(burrow)
            new_amphipod = Amphipod(amphipod.kind, move)
            del new_burrow.available[position]

            new_burrow.located[move] = new_amphipod
            # print(new_burrow)
            moves.append((cost, new_burrow))
        else:
            for move, cost in hallway_destinations:
                new_burrow = deepcopy(burrow)
                new_amphipod = Amphipod(amphipod.kind, move)
                del new_burrow.available[position]

                new_burrow.hallway[move] = new_amphipod
                moves.append((cost, new_burrow))

    return moves


def organize(burrow) -> bool:

    heap = []
    hq.heappush(heap, (0, burrow))
    visited = set()

    str_state = burrow.get_str_state()
    visited.add(str_state)
    cost_table = {str_state: 0}

    cycles: int = 0

    while heap:
        cycles += 1
        cost, burrow = hq.heappop(heap)

        current_str_state = burrow.get_str_state()

        # print(burrow)

        if burrow.is_organized():
            # print(burrow)
            print(f"{cycles = }")
            return cost

        for travel_cost, new_burrow in get_next_states(burrow):

            str_state = new_burrow.get_str_state()
            if str_state in visited:
                continue

            old_cost = cost_table.get(str_state, float("inf"))
            new_cost = cost_table[current_str_state] + travel_cost

            if new_cost < old_cost:
                # visited.add(str_state)
                # print("psuth")
                hq.heappush(heap, (new_cost, new_burrow))
                cost_table[str_state] = new_cost

        visited.add(current_str_state)

    return None


def solution(filename):
    burrow = parse(filename)
    return organize(burrow)


if __name__ == "__main__":
    # part 1 -----------------------------------------------------

    # result = solution("./data/example1.txt")  # should be 12521
    # print(result)

    result = solution("./data/input.txt")  # should be 18282
    print(result)
    
    # part 2 -----------------------------------------------------

    # result = solution("./data/example2.txt")  # should be 44169
    # print(result)

    result = solution("./data/input2.txt")
    print(result)
