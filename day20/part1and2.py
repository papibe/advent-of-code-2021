DARK = '0'
LIGHT = '1'


def get_neighbors_str(image, row, col, iteration):
    steps = [
        (-1,-1),
        (-1,0),
        (-1,1),
        (0,-1),
        (0,0),
        (0,1),
        (1,-1),
        (1,0),
        (1,1),
    ]
    bin_str = []
    for x, y in steps:
        if 0 <= row + x < len(image) and 0 <= col + y <len(image[0]):
            bin_str.append(image[row + x][col + y])
        else:
            if iteration % 2 == 0:
                bin_str.append(DARK)
            else:
                bin_str.append(LIGHT)

    return ''.join(bin_str)


def enhance(image, i, j, iea, iteration):
    str_index = get_neighbors_str(image, i - 1 , j - 1, iteration)
    return iea[int(str_index, 2)]


def process_image(image, iea, iteration):
    new_image = [['+'] * (len(image[0]) + 2) for _ in range(len(image) + 2)]
    
    for i, row in enumerate(new_image):
        for j, col in enumerate(row):
            new_image[i][j] = enhance(image, i, j, iea, iteration)

    return new_image


def solution(filename, times):
    with open(filename) as fp:
        raw_data0 = fp.read()

    # replace characters for usefull ones
    raw_data1 = raw_data0.replace('.', DARK)
    raw_data2 = raw_data1.replace('#', LIGHT)
    data = raw_data2.split('\n\n')

    # divide input data into blocks
    block1 = data[0].splitlines()   # image enhancement algorithm
    block2 = data[1].splitlines()   # input image

    # build image enhancement algorithm (iea) list
    iea = []
    for line in block1:
        iea.extend(list(line))

    # build input image matrix
    input_image = [list(line) for line in block2]

    image = input_image
    for iteration in range(times):
        image = process_image(image, iea, iteration)

    pixels = 0
    for row in image:
        for value in row:
            if value == LIGHT:
                pixels += 1

    return pixels

if __name__ == "__main__":
    result = solution("./data/input.txt", 2)
    print(result)

    result = solution("./data/input.txt", 50)
    print(result)
