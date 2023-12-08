import re
import math
from collections import defaultdict


def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    start_line = True
    wasteland_map = dict()
    ghosts = defaultdict(list)

    path = []
    for line in lines:
        if start_line is True:
            path = list(line)
            start_line = False
        elif len(line) == 0:
            continue
        else:
            match = re.search("(\w{3})\s*=\s*\((\w{3}),\s(\w{3})\)", line)
            if match.group(1)[2] == "A":
                ghosts[match.group(1)] = [match.group(1), 0, 0]

            wasteland_map[match.group(1)] = [match.group(2), match.group(3)]

    return path, wasteland_map, ghosts


def day8_part1(filename):
    path, wasteland_map, starting_nodes = parse_file(filename)

    total_moves = 0
    move_index = 0
    current_position = "AAA"
    while True:
        if path[move_index] == "L":
            current_position = wasteland_map[current_position][0]
        elif path[move_index] == "R":
            current_position = wasteland_map[current_position][1]

        move_index += 1
        if move_index % (len(path)) == 0:
            move_index = 0

        total_moves += 1

        if current_position == "ZZZ":
            break

    return total_moves


def day8_part2(filename):
    path, wasteland_map, ghosts = parse_file(filename)

    move_index = 0
    ghosts_done = []
    while True:
        for ghost in ghosts:
            if path[move_index] == "L":
                ghosts[ghost][0] = wasteland_map[ghosts[ghost][0]][0]
            elif path[move_index] == "R":
                ghosts[ghost][0] = wasteland_map[ghosts[ghost][0]][1]

            ghosts[ghost][1] += 1
            ghosts[ghost][2] += 1

            if ghosts[ghost][0][2] == "Z":
                ghosts_done.append(ghosts[ghost][1])

        move_index += 1
        if move_index % (len(path)) == 0:
            move_index = 0

        if len(ghosts) == len(ghosts_done):
            break

    return lcm_of_list(ghosts_done)


def lcm_of_list(numbers):
    def lcm(a, b):
        return abs(a * b) // math.gcd(a, b)

    lcm_result = 1
    for number in numbers:
        lcm_result = lcm(lcm_result, number)

    return lcm_result


if __name__ == '__main__':
    # print("part1: test_input=%s" % day8_part1('inputs/day8/test_input.txt'))
    print("part1: input=%s" % day8_part1('inputs/day8/input.txt'))
    #
    print("part2: test_input=%s" % day8_part2('inputs/day8/test_input.txt'))
    print("part2: input=%s" % day8_part2('inputs/day8/input.txt'))
