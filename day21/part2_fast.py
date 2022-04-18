from itertools import product

DIE_VALUES = [1, 2, 3]
NUM_ROLLS = 3
WIN_POINTS = 21

roll_universes = {}
for roll in [p for p in product(DIE_VALUES, repeat=NUM_ROLLS)]:
    roll_value = sum(roll)
    roll_universes[roll_value] = roll_universes.get(roll_value, 0) + 1

dp = {}


def dirac_dice_game(turn, pos1, score1, pos2, score2):
    if score1 >= WIN_POINTS:
        return (1, 0)
    if score2 >= WIN_POINTS:
        return (0, 1)

    if (turn, pos1, score1, pos2, score2) in dp:
        return dp[(turn, pos1, score1, pos2, score2)]

    current_score1 = 0
    current_score2 = 0

    for dice_score, die_universes in roll_universes.items():
        if turn == 1:
            new_pos1 = (pos1 - 1 + dice_score) % 10 + 1
            new_score1 = score1 + new_pos1
            next_score1, next_score2 = dirac_dice_game(
                2, new_pos1, new_score1, pos2, score2
            )

        else:
            new_pos2 = (pos2 - 1 + dice_score) % 10 + 1
            new_score2 = score2 + new_pos2
            next_score1, next_score2 = dirac_dice_game(
                1, pos1, score1, new_pos2, new_score2
            )

        current_score1 += next_score1 * die_universes
        current_score2 += next_score2 * die_universes

    dp[(turn, pos1, score1, pos2, score2)] = (current_score1, current_score2)
    return dp[(turn, pos1, score1, pos2, score2)]


def solution(pos1, pos2):
    wins1, wins2 = dirac_dice_game(1, pos1, 0, pos2, 0)
    return max(wins1, wins2)


if __name__ == "__main__":
    # in total both calls take about 0.08secs
    result = solution(4, 8)
    print(result)  # it should be 444356092776315

    result = solution(1, 5)
    print(result)
