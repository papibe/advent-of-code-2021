SPACE = 0
DOT = 1

def solution(filename):
    with open(filename) as fp:
        data = fp.read()

    blocks = data.split('\n\n')

    dots = [list(map(int, line.split(','))) for line in blocks[0].splitlines()]
    folds = [line.split()[-1].split('=') for line in blocks[1].splitlines()]

    ncols = max([x for x, y in dots]) + 1
    nrows = max([y for x, y in dots]) + 1

    paper = [[0] * ncols for _ in range(nrows)]
    for x, y in dots:
        paper[y][x] = 1

    dimension, str_value = folds[0]
    value = int(str_value)

    if dimension == 'y':
        new_nrows = value 

        # upper side remains the same
        new_paper = [['*'] * ncols for _ in range(new_nrows)]
        for i in range(len(new_paper)):
            for j in range(len(new_paper[0])):
                new_paper[i][j] = paper[i][j]
        # folding
        for i in range(nrows - value - 1):
            for j in range(len(new_paper[0])):
                new_paper[value - i - 1][j] = DOT if new_paper[value  - i - 1][j] == DOT or \
                    paper[value + i + 1][j] == DOT else SPACE

    if dimension == 'x':
        new_ncols = value 
        new_paper = [['*'] * new_ncols for _ in range(nrows)]

        # left side remains the same
        for i in range(len(new_paper)):
            for j in range(len(new_paper[0])):
                new_paper[i][j] = paper[i][j]
        # folding
        for i in range(len(new_paper)):
            for j in range(ncols - value - 1):
                new_paper[i][value - j - 1] = DOT if new_paper[i][value - j - 1] == DOT or \
                    paper[i][value + j + 1] == DOT else SPACE

    return sum(sum(row) for row in new_paper)


if __name__ == "__main__":
    result = solution("./data/example.txt")
    print(result)   # it should be 17

    result = solution("./data/input.txt")
    print(result)
