
def solution(filename):
    with open(filename) as fp:
        rawData = fp.readlines()

    # convert raw data to integer
    data = [int(line) for line in rawData]

    # loop over data keeping track of the previous value
    previous = data[0]

    counter = 0
    for current in data:
        if current > previous:
            counter += 1
        previous = current

    return counter

if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 7

    result = solution("./input.txt")
    print(result)
