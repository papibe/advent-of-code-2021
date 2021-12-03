
def solution(filename):
    with open(filename) as fp:
        data = fp.readlines()

    # Initial position and aim
    depth = 0
    horizontal = 0
    aim = 0

    # cycle over planned course
    for line in data:
        command, units = line.split()
        
        if command == "forward":
            horizontal += int(units)
            depth += aim * int(units)
        if command == "down":
            aim += int(units)
        if command == "up":
            aim -= int(units)

    return depth * horizontal

if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 900

    result = solution("./input.txt")
    print(result)
