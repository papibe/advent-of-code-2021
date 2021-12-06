
class BingoNumber:
    def __init__(self, number, marked=False):
        self.number = number
        self.marked = False
    
    def mark(self):
        self.marked = True

class BingoBoard:
    def __init__(self, matrix):
        self.board = [[BingoNumber(int(number)) for number in row] for row in matrix]

    def __str__(self):
        for row in self.board:
            for bnumber in row:
                if bnumber.marked:
                    print('*', end='')
                print(bnumber.number, end=' ')
            print()

        return ''


    def mark_number(self, number):
        for row in self.board:
            for bnumber in row:
                if bnumber.number == number:
                    bnumber.mark()


    def has_won(self):
        # check rows
        for row in self.board:
            win_row = True
            for bnumber in row:
                win_row = win_row and bnumber.marked
            if win_row:
                return True

        # check columns
        for j in range(len(self.board)):
            win_col = True
            for i in range(len(self.board[0])):
                win_col = win_col and self.board[i][j].marked
            if win_col:
                return True
        return False


    def sum_unmarked(self):
        sun = 0 # sum of unmarked numbers
        for row in self.board:
            for bnumber in row:
                if not bnumber.marked:
                    sun += bnumber.number
        return sun

def exhaust_bingo(loosers, random_numbers):

    for drawn_number in random_numbers:
        current_loosers = []
        for index, board in enumerate(loosers):
            board.mark_number(drawn_number)
            if not board.has_won():
                current_loosers.append(board)
            else:
                if len(loosers) ==  1:
                    return board, drawn_number
        loosers = current_loosers


def solution(filename):
    with open(filename) as fp:
        data = fp.read()

    # separate information
    data_blocks = data.split('\n\n')

    # get random numbers
    random_numbers = [int(number) for number in data_blocks[0].split(',')]

    # parse bingo boards
    bingo_boards = []
    for raw_board in data_blocks[1:]:
        board = [board_row.split() for board_row in raw_board.splitlines()]
        bingo_boards.append(BingoBoard(board))

    # play bingo!
    board, drawn_number = exhaust_bingo(bingo_boards[:], random_numbers)

    # calculate score:
    sum_unmarked_numbers = board.sum_unmarked()
    return sum_unmarked_numbers * drawn_number


if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 198

    result = solution("./input.txt")
    print(result)
