import numpy as np


def read_file_to_structure(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    cave = [[]]
    x_left = 10000
    x_right = 0
    y_top = 10000
    y_bottom = 0
    for line in lines:
        if line == '':
            continue
        coords = line.split(' -> ')
        for c in range(0, len(coords)-1):
            x1, y1 = [int(c) for c in coords[c].split(',')]
            x2, y2 = [int(c) for c in coords[c+1].split(',')]

            if x_left > min(x1, x2, x_left):
                x_left = min(x1, x2)
            if x_right < max(x1, x2, x_right):
                x_right = max(x1, x2)
            if y_top > min(y1, y2, y_top):
                y_top = min(y1, y2)
            if y_bottom < max(y1, y2, y_bottom):
                y_bottom = max(y1, y2)

            add_rock(cave, x1, x2, y1, y2)

    return cave, x_left, x_right, y_top, y_bottom


def add_rock(cave, x1, x2, y1, y2):
    rows = len(cave)
    cols = len(cave[0])
    if max(x1, x2) > cols or max(y1, y2) > rows:
        cave = resize_cave(cave, max(x1, x2), max(y1, y2), False)

    if y1 == y2:
        for c_x in range(sorted([x1, x2])[0], sorted([x1, x2])[1] + 1):
            cave[y1][c_x] = 1
    elif x1 == x2:
        for c_y in range(sorted([y1, y2])[0], sorted([y1, y2])[1] + 1):
            cave[c_y][x1] = 1
    return cave


def show_cave(cave, x1, x2, y1, y2):
    mapping = {0: '.', 1: '#', 2: 'o'}
    print("======")
    y_range = sorted([y1, y2])
    for y in range(0, y_range[1]+1):
        l = []
        x_range = sorted([x1, x2])
        for x in range(x_range[0]-1, x_range[1]+1):
            l.append(mapping[cave[y][x]])
        print(''.join(l))
    print("======")


def resize_cave(cave, x, y, is_bidirect):
    if y > len(cave):
        y_range = sorted([len(cave), y])
        for i_y in range(y_range[0], y_range[1]+1):
            x_line = [0] * (len(cave[0]))
            cave.append(x_line)

    if is_bidirect:
        for y_i in range(0, len(cave)):
            for x_i in range(0, x):
                cave[y_i].insert(0, 0)
                cave[y_i].append(0)
    else:
        if x > len(cave[0]):
            for y_i in range(0, len(cave)):
                x_range = sorted([len(cave[y_i]), x])
                for x in range(x_range[0], x_range[1]+1):
                    cave[y_i].append(0)
    return cave


def task1(filename):
    cave, x_left, x_right, y_top, y_bottom = read_file_to_structure(filename)

    sand_unit_counter = 0
    while True:
        sand_unit_counter += 1
        i = 0
        j = 500
        while True:
            if i+1 >= len(cave):
                return sand_unit_counter-1
            #show_cave(cave, x_left, x_right, y_top, y_bottom)
            if cave[i+1][j] == 0:
                cave[i][j] = 0
                cave[i + 1][j] = 2
                i += 1
                continue
            else:
                if cave[i+1][j-1] == 0:
                    cave[i][j] = 0
                    cave[i+1][j-1] = 2
                    i += 1
                    j -= 1
                    continue
                elif cave[i+1][j+1] == 0:
                    cave[i][j] = 0
                    cave[i+1][j+1] = 2
                    i += 1
                    j += 1
                    continue
                else:
                    cave[i][j] = 2
            break


def task2(filename):
    cave, x_left, x_right, y_top, y_bottom = read_file_to_structure(filename)
    add_ground = 500
    x1_floor = 0
    x2_floor = len(cave[0])-1 + add_ground
    y_floor = len(cave) + 1
    cave = add_rock(cave, x1_floor, x2_floor, y_floor, y_floor)
    cave = resize_cave(cave, add_ground, len(cave), True)
    show_cave(cave, x_left + add_ground-30, x_right+add_ground+30, y_top, y_bottom+2)

    sand_unit_counter = 0
    while True:
        sand_unit_counter += 1
        i = 0
        j = add_ground + 500
        while True:
            if i == 0 and cave[i][j] == 2:
                return sand_unit_counter - 1
            #show_cave(cave, x_left + add_ground - 30, x_right+add_ground + 30, y_top, y_bottom+2)
            if cave[i + 1][j] == 0:
                cave[i][j] = 0
                cave[i + 1][j] = 2
                i += 1
                continue
            else:
                if cave[i + 1][j - 1] == 0:
                    cave[i][j] = 0
                    cave[i + 1][j - 1] = 2
                    i += 1
                    j -= 1
                    continue
                elif cave[i + 1][j + 1] == 0:
                    cave[i][j] = 0
                    cave[i + 1][j + 1] = 2
                    i += 1
                    j += 1
                    continue
                else:
                    cave[i][j] = 2
            break



def day14():
    test1_result = task1('inputs/day14/test.txt')
    print("%d" % test1_result)

    task1_result = task1('inputs/day14/input.txt')
    print("%d" % task1_result)

    test2_result = task2('inputs/day14/test.txt')
    print("%s" % test2_result)

    task2_result = task2('inputs/day14/input.txt')
    print("%s" % task2_result)


if __name__ == '__main__':
    day14()