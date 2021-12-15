class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class List:
    def __init__(self):
        self.head = None
        self.tail = None
        self.frequency = {}

    def count(self, value):
        self.frequency[value] = self.frequency.get(value, 0) + 1

    def insert_at_end(self, value):
        node = ListNode(value)
        if self.head == None:
            self.head = node
            self.tail = node
        
        self.tail.next = node
        self.tail = node
        self.count(value)

    def insert_at(self, current, value):
        node = ListNode(value)
        temp = current.next
        current.next = node
        node.next = temp
        self.count(value)


    def to_string(self):
        output = []
        current = self.head
        while current is not None:
            output.append(current.value)
            current = current.next
        return ''.join(output)

    def copy(self):
        new_list = List()
        current = self.head
        while current is not None:
            new_list.insert_at_end(current.value)
            current = current.next
        return new_list

    def common_minus_least(self):
        return max(self.frequency.values()) - min(self.frequency.values())


def solution(filename, steps):
    with open(filename) as fp:
        data = fp.read()

    blocks = data.split('\n\n')

    initial_template = blocks[0]
    rules = {line.split(' -> ')[0]:line.split(' -> ')[1] for line in blocks[1].splitlines()}

    template = List()
    for char in initial_template:
        template.insert_at_end(char)

    for i in range(steps):
        new_template = template.copy()
        target = new_template.head
        next_target = target.next


        current = template.head
        next_node = current.next
        while next_node is not None:
            char_insert = rules[current.value + next_node.value]

            new_template.insert_at(target, char_insert)

            current = next_node
            next_node = next_node.next

            target = next_target
            next_target = target.next

        template = new_template

    return template.common_minus_least()


if __name__ == "__main__":
    result = solution("./data/example.txt", 10)
    print(result)   # it should be 1588

    result = solution("./data/input.txt", 10)
    print(result)
