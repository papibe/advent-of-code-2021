HEX_TO_BIN ={
    '0' :['0','0','0','0'],
    '1' :['0','0','0','1'],
    '2' :['0','0','1','0'],
    '3' :['0','0','1','1'],
    '4' :['0','1','0','0'],
    '5' :['0','1','0','1'],
    '6' :['0','1','1','0'],
    '7' :['0','1','1','1'],
    '8' :['1','0','0','0'],
    '9' :['1','0','0','1'],
    'A' :['1','0','1','0'],
    'B' :['1','0','1','1'],
    'C' :['1','1','0','0'],
    'D' :['1','1','0','1'],
    'E' :['1','1','1','0'],
    'F' :['1','1','1','1'],
}

LITERAL = 4


def get_package_type(bits, index):
    return int(bits[index] + bits[index + 1] + bits[index + 2], 2)


def get_version(bits, index):
    return int(bits[index] + bits[index + 1] + bits[index + 2], 2)


def get_literal(bits, index):
    value_bits = []
    block = bits[index:index+5]
    while block[0] == '1':
        value_bits.extend(block[1:])
        index += 5
        block = bits[index:index+5]
    value_bits.extend(block[1:])
    return index + 5, int(''.join(value_bits), 2)


def parse(bits, index, end):
    version_sum = 0
    while index < end - 7:
        version = get_version(bits, index)
        version_sum += version
        package_type = get_package_type(bits, index + 3)
        index += 6

        if package_type == LITERAL:
            index, value = get_literal(bits, index)
        else: # operator package
            length_type = bits[index]
            shift = 15 if length_type == '0' else 11
            index = index + 1 + shift

    return version_sum


def hex_to_bin(hexdata):
    bits = []
    for hexchar in hexdata:
        bits.extend(HEX_TO_BIN[hexchar])
    return bits


def solve_from_hex(string):
    bits = hex_to_bin(string)
    return parse(bits, 0, len(bits))


def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()[0]

    return solve_from_hex(data)


if __name__ == "__main__":
    result = solve_from_hex("D2FE28")
    print(result)   # it should be 6, lit value 2021

    result = solve_from_hex("38006F45291200")
    print(result)   # it should be 9

    result = solve_from_hex("EE00D40C823060")
    print(result)   # it should be 14

    result = solve_from_hex("8A004A801A8002F478")
    print(result)   # it should be 16

    result = solve_from_hex("620080001611562C8802118E34")
    print(result)   # it should be 12

    result = solve_from_hex("C0015000016115A2E0802F182340")
    print(result)   # it should be 23

    result = solve_from_hex("A0016C880162017C3686B18A3D4780")
    print(result)   # it should be 31

    result = solution("./data/input.txt")
    print(result)
