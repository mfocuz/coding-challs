def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    structure = []

    for line in lines:
        pass

    return structure

def dayN_part1(filename):
    data = parse_file(filename)

    return None


def dayN_part2(filename):
    data = parse_file(filename)

    return None


if __name__ == '__main__':
    print("part1: test_input=%s" % dayN_part1('inputs/<day5>/test_input.txt'))
    print("part1: input=%s" % dayN_part1('inputs/<day5>/input.txt'))

    print("part2: test_input=%s" % dayN_part2('inputs/<day5>/test_input.txt'))
    print("part2: input=%s" % dayN_part2('inputs/<day5>/input.txt'))
