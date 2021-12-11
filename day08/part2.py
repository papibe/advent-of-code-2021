from copy import deepcopy

length_to_unique_digits = {
    2: 1,
    4: 4,
    3: 7,
    7: 8
}
length_to_non_unique_digits = {
    5: [2, 3, 5],
    6: [0, 6, 9],
}
digit_to_wire = {
    0: [0, 1, 2, 4, 5, 6],
    1: [2, 5],
    2: [0, 2, 3, 4, 6],
    3: [0, 2, 3, 5, 6],
    4: [1, 2, 3, 5],
    5: [0, 1, 3, 5, 6],
    6: [0, 1, 3, 4, 5, 6],
    7: [0, 2, 5],
    8: [0, 1, 2, 3, 4, 5, 6],
    9: [0, 1, 2, 3, 5, 6],
}

wiring_to_digit = {
    (0, 1, 2, 4, 5, 6): '0',
    (2, 5): '1',
    (0, 2, 3, 4, 6): '2',
    (0, 2, 3, 5, 6): '3',
    (1, 2, 3, 5): '4',
    (0, 1, 3, 5, 6): '5',
    (0, 1, 3, 4, 5, 6): '6',
    (0, 2, 5): '7',
    (0, 1, 2, 3, 4, 5, 6): '8',
    (0, 1, 2, 3, 5, 6): '9',
}


def search_for_wiring(signals, wiring):

    # check if this path is not possible: if intersection was an empty set
    for wire in wiring:
        if len(wire) == 0:
            return None

    # check a win condition
    for wire in wiring:
        if len(wire) != 1:
            break
    else:
        if len(signals) == 0:
            winner = [item.pop() for item in wiring]
            return tuple(winner)

    while signals:
        value, digits = signals.pop()
        for digit in digits:
            try_wiring = deepcopy(wiring)
            for wire in range(7):
                if wire in digit_to_wire[digit]:
                    try_wiring[wire] &= set(value)
                else:
                    try_wiring[wire] -= set(value)
            new_signals = deepcopy(signals)
            dg = search_for_wiring(new_signals, try_wiring)
            if dg is not None:
                return dg

    return None



def line_solution(line):

    # parsing line
    raw_unique_signals, raw_output_values = line.split('|')
    unique_signals = raw_unique_signals.split()
    output_values = raw_output_values.split()

    display_wiring = [set(['a', 'b', 'c', 'd', 'e', 'f', 'g']) for _ in range(7)]

    # apply unique number restrictions
    for value in unique_signals + output_values:
        if len(value) in length_to_unique_digits:
            digit = length_to_unique_digits[len(value)]
            for wire in range(7):
                if wire in digit_to_wire[digit]:
                    display_wiring[wire] &= set(value)
                else:
                    display_wiring[wire] -= set(value)

    # for list of non unique values, and its possible solutions
    non_unique_signals = []
    for value in unique_signals + output_values:
        if len(value) in length_to_non_unique_digits:
            digits = length_to_non_unique_digits[len(value)]
            non_unique_signals.append((value, digits))

    # recursion tree on non unique numbers
    dg = search_for_wiring(non_unique_signals, deepcopy(display_wiring))

    translator = {char: idx for idx, char in enumerate(dg)}

    line_value = []
    for value in output_values:
        position_list = [translator[char] for char in value]
        position_list.sort()
        line_value.append(wiring_to_digit[tuple(position_list)])

    return int(''.join(line_value))


def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()

    return sum([line_solution(line) for line in data])


if __name__ == "__main__":
    result = solution("./data/example2.txt")
    print(result)   # it should be 5353

    result = solution("./data/example1.txt")
    print(result)   # it should be 61229

    result = solution("./data/input.txt")
    print(result)
