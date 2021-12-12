def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()

    closers = {')': '(', ']': '[', '}': '{', '>': '<'}
    points = {')': 3, ']': 57, '}': 1197, '>': 25_137}

    score = 0
    for line in data:
        stack = []
        for char in line:
            if char not in closers:
                stack.append(char)
                continue

            lastchar = stack.pop()
            if lastchar != closers[char]:
                score += points[char]
                break

    return score

if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 26397

    result = solution("./input.txt")
    print(result)
