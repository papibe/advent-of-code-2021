def fuel_comsuption(pos1, pos2):
    n = abs(pos1 - pos2)
    return n * (n + 1) // 2

def solution(filename):
    with open(filename) as fp:
        raw_data = fp.read()

    crab_positions = list(map(int, raw_data.split(',')))

    fuel_per_position = []
    for candidate_position in range(min(crab_positions), max(crab_positions)):
        current_fuel_comsuption = 0
        for crab_position in crab_positions:
            current_fuel_comsuption += fuel_comsuption(crab_position, candidate_position)
        fuel_per_position.append(current_fuel_comsuption)

    return min(fuel_per_position)

if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 168

    result = solution("./input.txt")
    print(result)
