def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    oasis = []

    for line in lines:
        oasis.append([int(x) for x in line.split(" ")])

    return oasis

def day9_part1(filename):
    oasis = parse_file(filename)

    result = []
    for line in oasis:
        extra = calc_next_layer(line)
        result.append(extra[len(extra)-1])

    return sum(result)


def calc_next_layer(line):
    differences = [line[i+1] - line[i] for i in range(len(line)-1)]

    if all(x == 0 for x in differences):
        line.append(line[len(line)-1])
        return line
    else:
        next_layer = calc_next_layer(differences)
        line.append(next_layer[len(next_layer) - 1] + line[len(line)-1])
        return line


def calc_next_layer_prev(line):
    differences = [line[i+1] - line[i] for i in range(len(line)-1)]

    if all(x == 0 for x in differences):
        line.insert(0, line[0])
        return line
    else:
        next_layer = calc_next_layer_prev(differences)
        line.insert(0, line[0] - next_layer[0])
        return line


def day9_part2(filename):
    oasis = parse_file(filename)

    result = []
    for line in oasis:
        extra = calc_next_layer_prev(line)
        result.append(extra[0])

    return sum(result)


if __name__ == '__main__':
    print("part1: test_input=%s" % day9_part1('inputs/day9/test_input.txt'))
    print("part1: input=%s" % day9_part1('inputs/day9/input.txt'))
    # #
    print("part2: test_input=%s" % day9_part2('inputs/day9/test_input.txt'))
    print("part2: input=%s" % day9_part2('inputs/day9/input.txt'))
