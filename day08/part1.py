def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()

    digits_length = {
        2: 1,
        4: 4,
        3: 7,
        7: 8
    }

    counter = 0
    for line in data:
        _, raw_output_values = line.split('|')
        output_values = raw_output_values.split()

        for ovalue in output_values:
            if len(ovalue) in digits_length:
                counter += 1

    return counter

if __name__ == "__main__":
    result = solution("./data/example1.txt")
    print(result)   # it should be 26

    result = solution("./data/input.txt")
    print(result)
