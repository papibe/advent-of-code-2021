def count_ones_and_zeros(candidates):
    one_counter = [0] * len(candidates[0])
    zero_counter = [0] * len(candidates[0])

    # cycle over the binary input
    for bnumber in candidates:
        # cycle over each bit of a binary string
        for idx, bit in enumerate(bnumber):
            if bit == '1':
                one_counter[idx] += 1
            else:
                zero_counter[idx] += 1

    return one_counter, zero_counter


def determine_keep_bit(ones, zeros, how_common, index):
    if how_common == 'most common':
        if ones[index] >= zeros[index]:
            return '1'
        else:
            return '0'
    else:   # 'least common'
        if zeros[index] <= ones[index]:
            return '0'
        else:
            return '1'


def filter_candidates(candidates, bit, index):
    filter_candidates = []
    for bnumber in candidates:
        if bnumber[index] == bit:
            filter_candidates.append(bnumber)
    
    return filter_candidates


def get_rating(candidates, how_common):
    index = 0
    while len(candidates) > 1:

        # count ones and zeros for the current candidates
        one_counter, zero_counter = count_ones_and_zeros(candidates)

        # determine common bit
        keep_bit = determine_keep_bit(one_counter, zero_counter, how_common, index)

        # remove binary strings that dont have the keep bit
        candidates = filter_candidates(candidates, keep_bit, index)

        index += 1

    # convert to decimal last reminding binary string number
    return int(''.join(candidates[0]), 2)


def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()

    oxygen_generator_rating = get_rating(data, 'most common')
    co2_scrubber_rating = get_rating(data, 'least common')

    return oxygen_generator_rating * co2_scrubber_rating

if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 230

    result = solution("./input.txt")
    print(result)
