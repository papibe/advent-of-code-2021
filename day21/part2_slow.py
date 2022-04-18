from itertools import product

DIE_VALUES = [1, 2, 3]
NUM_ROLLS = 3
WIN_POINTS = 21

roll_universes = {}
for roll in [p for p in product(DIE_VALUES, repeat=NUM_ROLLS)]:
    roll_value = sum(roll)
    roll_universes[roll_value] = roll_universes.get(roll_value, 0) + 1


def diract_dice_game(turn, pos1, score1, pos2, score2, universes):
    if score1 >= WIN_POINTS:
        return (universes, 0)
    if score2 >= WIN_POINTS:
        return (0, universes)

    current_score1 = 0
    current_score2 = 0

    for die_score, die_universes in roll_universes.items():
        if turn == 1:
            new_pos1 = (pos1 - 1 + die_score) % 10 + 1
            new_score1 = score1 + new_pos1
            next_score1, next_score2 = diract_dice_game(
                2, new_pos1, new_score1, pos2, score2, universes * die_universes
            )
        else:
            new_pos2 = (pos2 - 1 + die_score) % 10 + 1
            new_score2 = score2 + new_pos2
            next_score1, next_score2 = diract_dice_game(
                1, pos1, score1, new_pos2, new_score2, universes * die_universes
            )
        current_score1 += next_score1
        current_score2 += next_score2

    return (current_score1, current_score2)


def solution(pos1, pos2):
    wins1, wins2 = diract_dice_game(1, pos1, 0, pos2, 0, 1)
    return max(wins1, wins2)


if __name__ == "__main__":
    result = solution(4, 8) # it takes about 40secs
    print(result) # it should be 444356092776315

    result = solution(1, 5) # it takes about 15secs
    print(result)
