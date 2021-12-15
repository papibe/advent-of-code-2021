SPACE = ' '
DOT = '#'


def paper_to_string(paper):
    output = []
    for row in paper:
        for item in row:
            output.append(item)
        output.append('\n')
    return ''.join(output)


def solution(filename):
    with open(filename) as fp:
        data = fp.read()

    blocks = data.split('\n\n')

    dots = [list(map(int, line.split(','))) for line in blocks[0].splitlines()]
    folds = [line.split()[-1].split('=') for line in blocks[1].splitlines()]

    ncols = max([x for x, y in dots]) + 1
    nrows = max([y for x, y in dots]) + 1

    paper = [['.'] * ncols for _ in range(nrows)]
    for x, y in dots:
        paper[y][x] = DOT


    step = 1
    for dimension, str_value in folds:
        value = int(str_value)
        if dimension == 'y':
            new_nrows = value

            # if new_nrows != nrows - value - 1:
            #     print(f'WARNING: uneven folding up: step: {step}: current rows: {nrows}, split at: {value}', end=' ')
            #     print(f'upper side: {new_nrows} lower side: {nrows - value - 1}')

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

            # if new_ncols != ncols - value - 1:
            #     print(f'WARNING: uneven folding left: step: {step}: current cols: {ncols}, split at: {value}', end=' ')
            #     print(f'left side: {new_ncols} lower side: {ncols - value - 1}')
            
            # left side remains the same
            for i in range(len(new_paper)):
                for j in range(len(new_paper[0])):
                    new_paper[i][j] = paper[i][j]
            # folding
            for i in range(len(new_paper)):
                for j in range(ncols - value - 1):
                    new_paper[i][value - j - 1] = DOT if new_paper[i][value - j - 1] == DOT or \
                        paper[i][value + j + 1] == DOT else SPACE
        step += 1

        paper = new_paper
        nrows = len(paper)
        ncols = len(paper[0])

    return paper_to_string(paper)


if __name__ == "__main__":
    result = solution("./data/example.txt")
    print(result)   # it should be 0, or a square

    result = solution("./data/input.txt")
    print(result)
