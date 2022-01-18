from json import loads
from enum import Enum
from math import floor, ceil


class TreeType(Enum):
    NUMBER = 0
    COMPLEX = 1


class TreeNode:
    def __init__(self, node_type, level, value=None, parent=None):
        self.type = node_type
        self.level = level
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None

    def to_list(self):
        if self.type == TreeType.NUMBER:
            return self.value
        return [self.left.to_list(), self.right.to_list()]

    def __repr__(self):
        return f"{self.type = } {self.level = } {self.value = }"

    def add(self, tree):
        new_root = TreeNode(TreeType.COMPLEX, 0)
        new_root.left = self.left
        new_root.right = self.right

        self.left.parent = new_root
        self.right.parent = new_root

        new_root.parent = self
        self.left = new_root
        self.right = tree
        tree.parent = self
        self.level = -1
        self.increase_level()

    def increase_level(self):
        self.level += 1
        if self.left:
            self.left.increase_level()
        if self.right:
            self.right.increase_level()

    @classmethod
    def parse(cls, snumber, level=0):
        if isinstance(snumber, int):
            return TreeNode(TreeType.NUMBER, level, snumber)

        current = TreeNode(TreeType.COMPLEX, level)
        current.left = TreeNode.parse(snumber[0], level + 1)
        current.right = TreeNode.parse(snumber[1], level + 1)
        current.left.parent = current
        current.right.parent = current
        return current

    def get_next_node(self):
        current = self
        while current.parent is not None and current.parent.right == current:
            current = current.parent

        if current.parent is None:
            return None

        current = current.parent.right
        while current is not None and current.type != TreeType.NUMBER:
            current = current.left

        return current

    def get_previous_node(self):
        current = self
        while current.parent is not None and current.parent.left == current:
            current = current.parent

        if current.parent is None:
            return None

        current = current.parent.left
        while current is not None and current.type != TreeType.NUMBER:
            current = current.right

        return current

    def explode(self):
        node = self
        if node.type == TreeType.NUMBER:
            return False
        if (
            node.level >= 4
            and node.left.type == TreeType.NUMBER
            and node.right.type == TreeType.NUMBER
        ):
            parent = node.parent
            left_value = node.left.value
            right_value = node.right.value

            previous_node = node.left.get_previous_node()
            if previous_node:
                previous_node.value += left_value

            next_node = node.right.get_next_node()
            if next_node:
                next_node.value += right_value

            newnode = TreeNode(TreeType.NUMBER, node.level, 0, parent)
            if parent.left == node:
                parent.left = newnode
            else:
                parent.right = newnode

            return True

        if node.left.explode() or node.right.explode():
            return True

        return False

    def split(self):
        if self.type == TreeType.NUMBER and self.value >= 10:
            self.left = TreeNode(
                TreeType.NUMBER, self.level + 1, floor(self.value / 2), self
            )
            self.right = TreeNode(
                TreeType.NUMBER, self.level + 1, ceil(self.value / 2), self
            )
            self.type = TreeType.COMPLEX
            self.value = None

            return True

        if self.left is None or self.right is None:
            return False

        return self.left.split() or self.right.split()

    def reduces(self):
        while True:
            if self.explode():
                continue

            if self.split():
                continue

            break

    def magnitude(self):
        if self.type == TreeType.NUMBER:
            return self.value

        return (3 * self.left.magnitude()) + (2 * self.right.magnitude())


def solution(filename):
    with open(filename) as fp:
        data = fp.read().splitlines()

    list_data = [loads(line) for line in data]

    snumbers = []
    for raw_snumber in list_data:
        snumbers.append(TreeNode.parse(raw_snumber))

    snail_sum = snumbers[0]
    for index in range(1, len(snumbers)):
        snail_sum.add(snumbers[index])
        snail_sum.reduces()

    return snail_sum


if __name__ == "__main__":
    result = solution("./data/input.txt")
    print(result.magnitude())
