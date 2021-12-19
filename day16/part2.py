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

# package type
SUM = 0
PRODUCT = 1
MINIMUM = 2
MAXIMUM = 3
LITERAL = 4
GREATER_THAN = 5
LESS_THAN = 6
EQUAL_TO = 7

oper_to_name = {
    0: 'SUM',
    1: 'PRODUCT',
    2: 'MINIMUM',
    3: 'MAXIMUM',
    4: 'LITERAL',
    5: 'GREATER_THAN',
    6: 'LESS_THAN',
    7: 'EQUAL_TO',
}


class Operator:
    def __init__(self, type, arguments):
        self.type = type
        self.arguments = arguments

    def __repr__(self):
        return f'({self.type}:{self.arguments})'


def get_package_type(bits, index):
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


def parse(bits, index, max_args):
    expression_stack = []
    while index < len(bits) - 7 and max_args > 0:
        package_type = get_package_type(bits, index + 3)
        index += 6

        # operator package
        if package_type in [SUM, PRODUCT, MINIMUM, MAXIMUM, GREATER_THAN, LESS_THAN, EQUAL_TO]: 
            length_type = bits[index]
            index += 1
            if length_type == '0':
                shift = 15
                size_subpacket = int(''.join(bits[index:index + shift]), 2)
                index += shift
                _, result = parse(bits[index:index + size_subpacket], 0, float('inf'))
                operator = Operator(oper_to_name[package_type], 0)
                expression_stack.append([operator, result])

                index += size_subpacket
            else:
                shift = 11
                num_arguments = int(''.join(bits[index:index + shift]), 2)
                operator = Operator(oper_to_name[package_type], num_arguments)
                index, result = parse(bits, index + shift, num_arguments)
                expression_stack.append([operator, result])

        elif package_type == LITERAL:
            index, value = get_literal(bits, index)
            expression_stack.append(value)
        else:
            raise('What the helium!')

        max_args -= 1

    return index, expression_stack


def evaluate(exp):
    if isinstance(exp, int):
        return exp

    if isinstance(exp, list) and isinstance(exp[0], Operator):
        operator = exp[0]
        operands = exp[1]
        if operator.type == 'SUM':
            return sum(evaluate(operands))

        if operator.type == 'PRODUCT':
            product = 1
            for expression in evaluate(operands):
                product *= expression
            return product

        if operator.type == 'MINIMUM':
            return min(evaluate(operands))

        if operator.type == 'MAXIMUM':
            return max(evaluate(operands))

        if operator.type == 'LESS_THAN':
            return 1 if evaluate(operands[0]) < evaluate(operands[1]) else 0

        if operator.type == 'GREATER_THAN':
            return 1 if evaluate(operands[0]) > evaluate(operands[1]) else 0

        if operator.type == 'EQUAL_TO':
            return 1 if evaluate(operands[0]) == evaluate(operands[1]) else 0
    else:
        return [evaluate(expression) for expression in exp]

    raise("I don't like your expression!")


def hex_to_bin(hexdata):
    bits = []
    for hexchar in hexdata:
        bits.extend(HEX_TO_BIN[hexchar])
    return bits


def solve_from_hex(string):
    bits = hex_to_bin(string)
    _, expression = parse(bits, 0, float('inf'))

    return evaluate(expression)


def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()[0]

    return solve_from_hex(data)


if __name__ == "__main__":
    result = solve_from_hex("D2FE28")
    print(result)   # 2021

    result = solve_from_hex("38006F45291200")
    print(result)   # 0

    result = solve_from_hex("EE00D40C823060")
    print(result)   # it should be 3

    result = solve_from_hex("C200B40A82")
    print(result)   # it should be 3

    result = solve_from_hex("04005AC33890")
    print(result)   # it should be 54

    result = solve_from_hex("880086C3E88112")
    print(result)   # it should be 7

    result = solve_from_hex("CE00C43D881120")
    print(result)   # it should be 9

    result = solve_from_hex("D8005AC2A8F0")
    print(result)   # it should be 1

    result = solve_from_hex("F600BC2D8F")
    print(result)   # it should be 0

    result = solve_from_hex("9C005AC2F8F0")
    print(result)   # it should be 0

    result = solve_from_hex("9C0141080250320F1802104A08")
    print(result)   # it should be 1

    result = solution("./data/input.txt")
    print(result)
