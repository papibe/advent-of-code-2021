WIN_POINTS = 1000


def die_rolls():
    value = 1
    while True:
        yield value
        value = (value) % 100 + 1


def solution(position1, position2):
    game_die_iterator = die_rolls()

    def die():
        return next(game_die_iterator)

    score1 = score2 = 0
    rolled_dice = 0

    while True:
        dice1 = die() + die() + die()
        position1 = (position1 - 1 + dice1) % 10 + 1
        score1 += position1
        rolled_dice += 3
        if score1 >= WIN_POINTS:
            return rolled_dice * score2

        dice2 = die() + die() + die()
        position2 = (position2 - 1 + dice2) % 10 + 1
        score2 += position2
        rolled_dice += 3
        if score2 >= WIN_POINTS:
            return rolled_dice * score1


if __name__ == "__main__":
    result = solution(4, 8)
    print(result)  # it should be 739785

    result = solution(1, 5)
    print(result)
