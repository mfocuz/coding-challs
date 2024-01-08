def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    patterns = []

    pattern = []
    for line in lines:
        if len(line) == 0:
            patterns.append(pattern)
            pattern = []
            continue

        line_elems = []
        for c in line:
            line_elems.append(c)
        pattern.append(line_elems)

    if len(pattern) > 0:
        patterns.append(pattern)

    return patterns


def find_mediana(pattern):
    horizontal = None
    vertical = None

    for i in range(0, len(pattern) - 1):
        if pattern[i] == pattern[i+1]:
            horizontal = i
            break

    for i in range(0, len(pattern[0])-1):
        vertical_str = ""
        for line in pattern:
            vertical_str += line[i]

        vertical_str_next = ""
        for line in pattern:
            vertical_str_next += line[i + 1]
        if vertical_str == vertical_str_next:
            vertical = i
            break

    return horizontal, vertical


def day13_part1(filename):
    patterns = parse_file(filename)
    results = []

    for pattern in patterns:
        horiz_mediana, vert_mediana = find_mediana(pattern)

        reflect_score = 0

        if horiz_mediana is not None:
            for line_i in range(horiz_mediana + 1):
                line = "".join(pattern[horiz_mediana - line_i])
                reflected_line = "".join(pattern[horiz_mediana + line_i + 1])
                if line != reflected_line:
                    break
                if horiz_mediana - line_i == 0 or horiz_mediana + line_i + 1 == len(pattern) - 1:
                    reflect_score += (horiz_mediana + 1) * 100
                    break

        if vert_mediana is not None:
            for column_i in range(vert_mediana+1):
                line_str = ""
                for line in pattern:
                    line_str += line[vert_mediana - column_i]

                line_reflected = ""
                for line in pattern:
                    line_reflected += line[vert_mediana + column_i + 1]

                if line_str != line_reflected:
                    break

                if vert_mediana - column_i == 0 or vert_mediana + column_i + 1 == len(pattern[0]) - 1:
                    reflect_score += vert_mediana + 1
                    break

        results.append(reflect_score)

    return sum(results)


def day13_part2(filename):
    data = parse_file(filename)

    return None


if __name__ == '__main__':
    # print("part1: test_input=%s" % day13_part1('inputs/day13/test_input.txt'))
    print("part1: input=%s" % day13_part1('inputs/day13/input.txt'))
    #
    # print("part2: test_input=%s" % day13_part2('inputs/day13/test_input.txt'))
    # print("part2: input=%s" % day13_part2('inputs/day13/input.txt'))
