import re
import sys

def run_alu(instructions, model_number):
    model_number_index = 0
    variables = { 'w': 0, 'x': 0, 'y': 0, 'z': 0 }

    for line in instructions:

        parsed_instruction = line.split()
        instruction = parsed_instruction[0]
        variable = parsed_instruction[1]

        if instruction == '#':
            continue

        if instruction == "inp":
            variables[variable] = int(model_number[model_number_index])
            model_number_index += 1
            continue

        parameter2 = parsed_instruction[2]
        if parameter2 in variables:
            operand = variables[parameter2]
        else:
            operand = int(parameter2)
       
        if instruction == "add":
            variables[variable] += operand

        elif instruction == "mul":
            variables[variable] *= operand

        elif instruction == "div":
            variables[variable] //= operand

        elif instruction == "mod":
            variables[variable] %= operand

        elif instruction == "eql":
            if variables[variable] == operand:
                variables[variable] = 1
            else:
                variables[variable] = 0
        else:
            raise('operation not allowed')

    return variables['z'] == 0

def solution(filename):
    
    with open(filename) as fp:
        instructions = fp.read().splitlines()

    model = [0] * 14
    valid_models = []

    for w0 in range(6, 1 - 1, -1):
        for w1 in range(5, 1 - 1, -1):
            for w2 in range(9, 2 - 1, -1):
                for w4 in range(4, 1 - 1, -1):
                    for w6 in range(1, 1 - 1, -1):
                        for w10 in range(7, 1 - 1, -1):
                            for w11 in range(9, 7 - 1, -1):
                                model[0] = w0
                                model[1] = w1
                                model[2] = w2
                                model[4] = w4
                                model[6] = w6
                                model[10] = w10
                                model[11] = w11

                                model[3] = w2 - 1
                                model[5] = w4 + 5
                                model[7] = w6 + 8
                                model[8] = w1 + 4
                                model[9] = w0 + 3
                                model[12] = w11 - 6
                                model[13] = w10 + 2

                                str_model = ''.join(map(str, model))

                                if run_alu(instructions, ''.join(str_model)):
                                    valid_models.append(str_model)

    return valid_models[0], valid_models[-1]

if __name__ == "__main__":
    result = solution("./data/input.txt")
    print(result)
