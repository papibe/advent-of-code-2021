READY_GIVE_BIRTH = 0

def solution(filename, days):
    with open(filename) as fp:
        raw_data = fp.read()

    fish_list = list(map(int, raw_data.split(',')))

    for day in range(days):
        newborns = []
        new_fish_list = []
        for fish in fish_list:
            if fish == READY_GIVE_BIRTH:
                new_fish_list.append(6)
                newborns.append(8)
            else:
                new_fish_list.append(fish - 1)
        new_fish_list.extend(newborns)
        fish_list = new_fish_list

    return len(fish_list)

if __name__ == "__main__":
    result = solution("./example.txt", 18)
    print(result)   # it should be 26

    result = solution("./example.txt", 80)
    print(result)   # it should be 5934

    result = solution("./input.txt", 80)
    print(result)
