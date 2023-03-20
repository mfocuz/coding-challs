import string
import random
import sys


class Node:
    def __init__(self, value, _hash):
        self.prev = None
        self.next = None
        self.value = value
        self.hash = _hash


class LinkedList:
    def __init__(self):
        start_node = Node('start', None)
        self.start_node = None
        self.zero_node = None
        self.current_node = start_node
        self.hash_list = []

    def add_node(self, value):
        _hash = str(value) + '-' + ''.join(random.choice(string.ascii_letters) for i in range(25))
        new_node = Node(value, _hash)
        new_node.prev = self.current_node
        new_node.prev.next = new_node
        new_node.next = None
        self.hash_list.append(_hash)
        self.current_node = new_node

        if self.start_node is None:
            self.start_node = new_node

        if value == 0:
            self.zero_node = new_node

    def complete(self):
        check_prev = self.current_node
        while check_prev.prev.value != 'start':
            check_prev = check_prev.prev
        self.current_node.next = check_prev
        check_prev.prev = self.current_node

    def find(self, _hash):
        node = self.start_node
        while True:
            if node.hash == _hash:
                return node
            node = node.next

        return node

    def find_by_offset(self, offset):
        node = self.zero_node
        for i in range(offset):
            node = node.next
        return node.value

    def move_right(self, _hash, node):
        moves = abs(node.value) % (len(self.hash_list) - 1)

        if moves == 0:
            return

        target_node = node
        for i in range(moves):
            target_node = target_node.next

        temp = target_node.next
        target_node.next.prev = node
        target_node.next = node

        node.prev.next = node.next
        node.next.prev = node.prev

        node.prev = target_node
        node.next = temp

    def move_left(self, _hash, node):
        moves = abs(node.value) % (len(self.hash_list)-1)

        if moves == 0:
            return

        node_target = node
        for i in range(moves):
            node_target = node_target.prev

        temp = node_target.prev
        node_target.prev.next = node
        node_target.prev = node

        node.next.prev = node.prev
        node.prev.next = node.next

        node.next = node_target
        node.prev = temp

    def get_hash_list(self):
        return self.hash_list

    def print_list(self):
        current_node = self.start_node.next
        line = ""
        count = len(self.hash_list)
        for i in range(count):
            print("%d <= %d => %d" % (current_node.prev.value, current_node.value, current_node.next.value))
            line += str(current_node.value) + ","
            current_node = current_node.next
        print(line)


def read_file_to_structure(filename, key=1):
    with open(filename) as f:
        lines = f.read().splitlines()

    code_list = LinkedList()
    for line in lines:
        code_list.add_node(int(line) * key)
    code_list.complete()

    if len(code_list.get_hash_list()) != len(lines):
        print("collision")
        sys.exit(0)

    return code_list


def task1(filename):
    code_list = read_file_to_structure(filename)
    for _hash in code_list.get_hash_list():
        node = code_list.find(_hash)
        if node.value >= 0:
            code_list.move_right(_hash, node)
        else:
            code_list.move_left(_hash, node)
        #code_list.print_list()

    c1 = code_list.find_by_offset(1000)
    c2 = code_list.find_by_offset(2000)
    c3 = code_list.find_by_offset(3000)

    return c1 + c2 + c3

def task2(filename):
    code_list = read_file_to_structure(filename, 811589153)
    for i in range(10):
        j = 0
        for _hash in code_list.get_hash_list():
            node = code_list.find(_hash)
            if node.value >= 0:
                code_list.move_right(_hash, node)
            else:
                code_list.move_left(_hash, node)
            if j % 100 == 0:
                print("i=%d; j=%d" % (i, j))
            j += 1

    c1 = code_list.find_by_offset(1000)
    c2 = code_list.find_by_offset(2000)
    c3 = code_list.find_by_offset(3000)

    return c1 + c2 + c3


def day20():
    # test1_result = task1('inputs/day20/test.txt')
    # print("result=%d" % test1_result)
    #
    # task1_result = task1('inputs/day20/input.txt')
    # print("%d" % task1_result)
    #
    # test2_result = task2('inputs/day20/test.txt')
    # print("%s" % test2_result)
    #
    task2_result = task2('inputs/day20/input.txt')
    print("%s" % task2_result)


if __name__ == '__main__':
    day20()