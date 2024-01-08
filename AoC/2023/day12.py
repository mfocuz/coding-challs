import re
# from itertools import permutations

def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    records = dict()

    for line in lines:
        r = line.split(" ")
        records[r[0]] = [int (x) for x in r[1].split(',')]

    return records


def find_potential_groups(springs, damaged_group):
    potential_groups = []
    state = "SEARCH"
    damaged_count = 0
    for i in range(len(springs)):
        if springs[i] == ".":
            state = "OPERATIONAL"
        elif springs[i] == "#" or springs[i] == "?":
            state = "DAMAGED"

        if state == "OPERATIONAL":
            potential_groups.append(damaged_count)
            damaged_count = 0
        elif state == "DAMAGED":
            damaged_count += 1

    if state == "DAMAGED":
        potential_groups.append(damaged_count)

    return potential_groups


def find_arrangements(springs, record, potential_groups):
    arrangements = 0
    for group in potential_groups:
        # find how many spring groups can be in this group
        spring_groups_inside = []
        for spring_group in record:
            if sum(spring_groups_inside) > record:
                break


def permutations(sequence):
    if len(sequence) == 0:
        return [[]]

    result = []
    for i in range(len(sequence)):
        first_element = sequence[i]
        remaining_elements = sequence[:i] + sequence[i + 1:]
        for perm in permutations(remaining_elements):
            result.append([first_element] + perm)

    return result


def find_permutations(springs, record):
    arrangements = dict()
    operational = ["."] * (len(springs) - sum(record))
    damaged = ["#" * x for x in record]

    perms = permutations(operational + damaged)


    for perm in perms:
        block_order = [x for x in perm if x != "."]
        to_break = False
        for i in range(len(block_order)):
            if record[i] != len(block_order[i]):
                to_break = True
                break
        if to_break:
            continue
        if check_if_match(springs.replace('.', '\.').replace('?','[#\.]'), ''.join(perm)):
            arrangements[perm] = True

    return len(arrangements)


def check_if_match(regexp, perm):
    print(perm)
    if re.match(regexp, perm):
        return True
    else:
        return False


def day12_part1(filename):
    records = parse_file(filename)

    arrangements = []
    for record in records:
        find_permutations(record, records[record])


    return sum(arrangements)


def day12_part2(filename):
    data = parse_file(filename)

    return None


if __name__ == '__main__':
    print("part1: test_input=%s" % day12_part1('inputs/day12/test_input.txt'))
    # print("part1: input=%s" % day12_part1('inputs/day12/input.txt'))
    #
    # print("part2: test_input=%s" % day12_part2('inputs/day12/test_input.txt'))
    # print("part2: input=%s" % day12_part2('inputs/day12/input.txt'))
