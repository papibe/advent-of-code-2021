def solution(position1, position2):
    score1 = score2 = 0
    play = 0
    rolled_dice = 0

    while True:
        dice1 = 3 * (6 * play + 2)
        position1 = (position1 - 1 + dice1) % 10 + 1
        rolled_dice += 3
        score1 += position1
        if score1 >= 1000:
            looser_score = score2
            break

        dice2 = 3 * (6 * play + 5)
        position2 = (position2 - 1 + dice2) % 10 + 1
        score2 += position2
        rolled_dice += 3
        if score2 >= 1000:
            looser_score = score1
            break

        play += 1

    return rolled_dice  * looser_score


if __name__ == "__main__":
    result = solution(4, 8)
    print(result)

    result = solution(1, 5)
    print(result)
