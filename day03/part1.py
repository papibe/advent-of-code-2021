
def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()
    
    # initialize rate counter
    one_counter = [0] * len(data[0])
    zero_counter = [0] * len(data[0])

    # cycle over the binary input
    for bnumber in data:

        # cycle over each bit of a binary string
        for index, bit in enumerate(bnumber):
            if bit == '1':
                one_counter[index] += 1
            else:
                zero_counter[index] += 1

    # determine gamma and epsilon rates
    gamma_rate = []
    epsilon_rate = []
    for i in range(len(data[0])):
        if one_counter[i] > zero_counter[i]:
            gamma_rate.append('1')
            epsilon_rate.append('0')
        else:
            gamma_rate.append('0')
            epsilon_rate.append('1')

    # convert binary strings to integer
    gamma = int(''.join(gamma_rate), 2)
    epsilon = int(''.join(epsilon_rate), 2)

    return gamma * epsilon

if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 198

    result = solution("./input.txt")
    print(result)
