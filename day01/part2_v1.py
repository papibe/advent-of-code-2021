
def solution(filename):
    with open(filename) as fp:
        rawData = fp.readlines()

    # convert raw data to integer
    data = [int(line) for line in rawData]

    # create a new list with the three-measurement sliding window values
    window_values = []
    for i in range(len(data) - 2):
        window_values.append(data[i] + data[i + 1] + data[i + 2])

    # loop over the new window data keeping track of the previous value
    previous = window_values[0]
    counter = 0
    for current in window_values:
        if current > previous:
            counter += 1
        previous = current

    return counter

if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 5

    result = solution("./input.txt")
    print(result)
