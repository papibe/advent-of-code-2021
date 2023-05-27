# Research material:
# http://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
# https://stackoverflow.com/questions/16452383/how-to-get-all-24-rotations-of-a-3-dimensional-array
# https://numpy.org/doc/stable/reference/generated/numpy.matmul.html
# https://stackoverflow.com/questions/21562986/numpy-matrix-vector-multiplication
# https://numpy.org/doc/stable/reference/generated/numpy.ndarray.tolist.html
# https://numpy.org/doc/stable/reference/generated/numpy.ndarray.astype.html
# https://stackoverflow.com/questions/10580676/comparing-two-numpy-arrays-for-equality-element-wise

from itertools import permutations, product
import numpy as np
import numpy.typing as npt
from collections import deque
from typing import Dict, Tuple, List, Set, Deque


def rotations(array: npt.ArrayLike) -> npt.ArrayLike:
    """Generator that produces all 24 space rotations"""
    for x, y, z in permutations([0, 1, 2]):
        for sx, sy, sz in product([-1, 1], repeat=3):
            rotation_matrix = np.zeros((3, 3), dtype=int)
            rotation_matrix[0, x] = sx
            rotation_matrix[1, y] = sy
            rotation_matrix[2, z] = sz
            if np.linalg.det(rotation_matrix) == 1:
                yield np.matmul(array, rotation_matrix)


def parse(filename: str) -> npt.ArrayLike:
    """Parse content of input file and return an NP array of scaned data"""
    with open(filename) as fp:
        data: List[List[str]] = fp.read().split("\n\n")

    scanner_data: List[npt.ArrayLike] = []
    for block in data:
        scanner_positions = block.splitlines()
        positions: List[List[str]] = []
        for line in scanner_positions[1:]:
            positions.append(line.split(","))
        scanner_data.append(np.matrix(positions, dtype=int))

    return scanner_data


def solution(filename: str) -> Tuple[int, int]:
    """
    Determine both the number of beacons and the largest Manhattan
    distance between any two scanners
    """
    # parse file
    scanner_data: List[npt.ArrayLike] = parse(filename)

    # calculate all 25 transformacions for all scanners
    all_transformations: List[List[npt.ArrayLike]] = []
    for _, scanner in enumerate(scanner_data):
        all_transformations.append([trans for trans in rotations(scanner)])

    # scanner 0 will be consider at position (0, 0, 0) and corrent (no transformation)
    fixed_scanners: Dict[int, npt.ArrayLike] = {0: scanner_data[0]}

    # all other scanners
    unfixed_scanners: Set[int] = set(range(1, len(scanner_data)))

    # where the coordinates of the discovered scanners will be
    scanner_coodinates: Set[Tuple[int, int, int]] = set()

    # BFS-like loop
    queue: Deque = deque([(0, scanner_data[0])])
    while queue:

        base_scanner_index, base_scanner = queue.pop()

        # look for every unfixed scanner transformations that has 12 common points
        for scanner_index in list(unfixed_scanners):
            for tindex, transformation in enumerate(all_transformations[scanner_index]):
                trans_rows, _ = transformation.shape

                # calculate (and count) the coordinates differences
                diffs: Dict[int, npt.ArrayLike] = {}
                for base_row in base_scanner:
                    for trans_row in transformation:
                        d: npt.ArrayLike = base_row - trans_row
                        key: Tuple[int, int, int] = (d[0, 0], d[0, 1], d[0, 2])
                        diffs[key] = diffs.get(key, 0) + 1

                # if there are 12 points in common add it to the queue
                # remove it from unfixed, and remember scanner coordinates
                for diff, value in diffs.items():
                    if value >= 12:
                        # print(
                        #     f"scanner {scanner_index:2} has {value} points in common with scanner {base_scanner_index:2} under transformation {tindex:2}"
                        # )
                        scanner_coodinates.add(diff)
                        diff_shift: npt.npt.ArrayLike = np.tile(diff, (trans_rows, 1))
                        fixed_scanners[scanner_index] = transformation + diff_shift
                        unfixed_scanners.remove(scanner_index)
                        queue.append((scanner_index, fixed_scanners[scanner_index]))
                        break

    # calculate the number of unique coordinates of the beacons
    total_coordinates: Set[Tuple[int, int, int]] = set()
    for scanner_index, scanner in fixed_scanners.items():
        for row in scanner:
            total_coordinates.add(tuple(*np.ndarray.tolist(row)))

    # calculate the max Manhattan distance between scanners
    max_distance: int = float("-inf")
    for x1, y1, z1 in scanner_coodinates:
        for x2, y2, z2 in scanner_coodinates:
            max_distance = max(abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2), max_distance)

    return len(total_coordinates), max_distance


if __name__ == "__main__":
    print(solution("./data/example2.txt"))  # (79, 3621)
    print(solution("./data/input.txt"))
