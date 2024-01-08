def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    field = []

    for line in lines:
        row = [c for c in line]
        field.append(row)

    return field


def day14_part1(filename):
    field = parse_file(filename)

    no_more_changes = False
    while True:
        if no_more_changes is True:
            break

        no_more_changes = True

        for row in range(len(field)):
            if row == 0:
                continue

            for col in range(len(field[row])):
                if field[row][col] != "O":
                    continue

                if field[row-1][col] == ".":
                    field[row][col] = "."
                    field[row-1][col] = "O"
                    no_more_changes = False

    return calc_score(field)


def calc_score(field):
    score = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "O":
                score += len(field) - i
    return score


def find_rocks(field):
    rocks_col = dict()
    rocks_row = dict()
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "#":
                rocks_col[j] = i
                rocks_row[i] = j

    return rocks_col, rocks_row


def display(field):
    for i in range(len(field)):
        line = ""
        for j in range(len(field[i])):
            line += field[i][j]
        print(line)


def day14_part2(filename):
    pass


if __name__ == '__main__':
    # print("part1: test_input=%s" % day14_part1('inputs/day14/test_input.txt'))
    # print("part1: input=%s" % day14_part1('inputs/day14/input.txt'))
    #
    print("part2: test_input=%s" % day14_part2('inputs/day14/test_input.txt'))
    # print("part2: input=%s" % day14_part2('inputs/day14/input.txt'))
