READY_GIVE_BIRTH = 0

def solution(filename, days):
    with open(filename) as fp:
        raw_data = fp.read()

    fish_list = list(map(int, raw_data.split(',')))
    current_generation = {
        0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0
    }
    for fish_timer in fish_list:
        current_generation[fish_timer] += 1

    for _ in range(days):
        next_generation = {
            0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0
        }
        for fish_timer, number_fish in current_generation.items():
            if fish_timer == READY_GIVE_BIRTH:
                next_generation[8] += number_fish
                next_generation[6] += number_fish
            else:
                next_generation[fish_timer - 1] += number_fish
        
        current_generation = next_generation

    return sum(current_generation.values())

if __name__ == "__main__":
    result = solution("./example.txt", 256)
    print(result)   # it should be 26984457539

    result = solution("./input.txt", 256)
    print(result)
