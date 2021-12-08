
BOARD_SIZE = 5

class BingoBoard:
    def __init__(self, matrix):
        total_sum = 0
        self.board_numbers = {}
        for i, row in enumerate(matrix):
            for j, number in enumerate(row):
                self.board_numbers[number] = (i, j)
                total_sum += number
        self.total_sum = total_sum
        self.row_counter = [0] * len(matrix)
        self.col_counter = [0] * len(matrix)

    def __str__(self):
        print(self.total_sum)
        print(self.row_counter)
        print(self.col_counter)
        return ''

    def mark_number(self, number):
        if number not in self.board_numbers:
            return False

        row, col = self.board_numbers[number]
        self.total_sum -= number
        self.row_counter[row] += 1
        self.col_counter[col] += 1
        if self.row_counter[row] == BOARD_SIZE or self.col_counter[col] == BOARD_SIZE:
            return True

        return False

def exhaust_bingo(loosers, random_board_numbers):

    for drawn_number in random_board_numbers:
        current_loosers = []
        for index, board in enumerate(loosers):
            if not board.mark_number(drawn_number):
                current_loosers.append(board)
            else:
                if len(loosers) ==  1:
                    return board, drawn_number
        loosers = current_loosers
    return None, None


def solution(filename):
    with open(filename) as fp:
        data = fp.read()

    # separate information
    data_blocks = data.split('\n\n')

    # get random board_numbers
    random_board_numbers = [int(number) for number in data_blocks[0].split(',')]

    # parse bingo boards
    bingo_boards = []
    for raw_board in data_blocks[1:]:
        board = [list(map(int, board_row.split())) for board_row in raw_board.splitlines()]
        bingo_object = BingoBoard(board)
        # print(bingo_object)
        bingo_boards.append(bingo_object)

    # play bingo!
    board, drawn_number = exhaust_bingo(bingo_boards[:], random_board_numbers)

    # calculate score:
    sum_unmarked_board_numbers = board.total_sum
    return sum_unmarked_board_numbers * drawn_number


if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 198

    result = solution("./input.txt")
    print(result)
