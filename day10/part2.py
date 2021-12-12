def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()

    closers = {')': '(', ']': '[', '}': '{', '>': '<'}
    openers = {'(': ')', '[': ']', '{': '}', '<': '>'}
    points = {')': 1, ']': 2, '}': 3, '>': 4}

    scores = []
    for line in data:
        stack = []
        for char in line:
            if char not in closers:
                stack.append(char)
                continue

            lastchar = stack.pop()
            if lastchar != closers[char]:
                break
        else:
            # incomplete line
            score = 0
            while stack:
                char = stack.pop()
                score = (score * 5) + points[openers[char]]

            scores.append(score)
    
    scores.sort()
    return scores[len(scores) // 2]

if __name__ == "__main__":
    result = solution("./example.txt")
    print(result)   # it should be 288957

    result = solution("./input.txt")
    print(result)
