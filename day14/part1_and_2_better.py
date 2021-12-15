def solution(filename, steps):
    with open(filename) as fp:
        data = fp.read()

    blocks = data.split('\n\n')

    initial_template = blocks[0]
    rules = {line.split(' -> ')[0]:line.split(' -> ')[1] for line in blocks[1].splitlines()}

    template = {}
    for i in range(len(initial_template) - 1):
        key = initial_template[i] + initial_template[i + 1]
        template[key] = template.get(key, 0) + 1

    counter = {}
    for letter in initial_template:
        counter[letter] = counter.get(letter, 0) + 1

    for step in range(steps):
        new_template = {}
        for key, value in template.items():
            new_key1 = key[0] + rules[key]
            new_template[new_key1] = new_template.get(new_key1, 0) + value

            new_key2 = rules[key] + key[1]
            new_template[new_key2] = new_template.get(new_key2, 0) + value

            counter[rules[key]] = counter.get(rules[key], 0) + value

        template = new_template

    return max(counter.values()) - min(counter.values())


if __name__ == "__main__":
    # part 1
    result = solution("./data/example.txt", 10)
    print(result)   # it should be 1588

    result = solution("./data/input.txt", 10)
    print(result)

    # part 2
    result = solution("./data/example.txt", 40)
    print(result)   # it should be 2188189693529

    result = solution("./data/input.txt", 40)
    print(result)
