import string

import numpy as np


def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    y = len(lines)
    x = len(lines[0].rstrip())

    engine = []

    for i in range(0, len(lines)):
        line_row = lines[i].rstrip()
        engine_row = []
        for j in range(0, len(line_row)):
            engine_row.append(line_row[j])
        engine.append(engine_row)

    return engine

def day2_part1(filename):
    engine = parse_file(filename)

    state = "EMPTY"
    adjacent_parts = []

    part_number = ""
    part_coordinates = []
    for y in range(0, len(engine)):
        for x in range(0, len(engine[y])):
            if (engine[y][x]).isdigit():
                if state == "EMPTY":
                    state = "PART"
                part_number += engine[y][x]
                part_coordinates.append([y,x])
            else:
                if engine[y][x] == '.':
                    if state == "PART":
                        if check_if_part_adjacent(engine, part_coordinates):
                            adjacent_parts.append(int(part_number))
                        part_number = ""
                        part_coordinates = []
                        state = "EMPTY"
                    elif state == "EMPTY":
                        continue
                elif is_spec_char(engine[y][x]):
                    if state == "PART":
                        state = "EMPTY"
                        adjacent_parts.append(int(part_number))
                        part_number = ""
                        part_coordinates = []
                    elif state == "EMPTY":
                        continue
    return sum(adjacent_parts)

def check_if_part_adjacent(engine, part_coord):
    for coord in part_coord:
        y = coord[0]
        x = coord[1]

        if (y != 0 and x != 0 and is_spec_char(engine[y-1][x-1])) or (y != 0 and is_spec_char(engine[y-1][x])) or (y != 0 and x != ((len(engine[0])-1)) and is_spec_char(engine[y-1][x+1])) \
            or (y != (len(engine)-1) and x != 0 and is_spec_char(engine[y+1][x-1])) or (y != (len(engine)-1) and is_spec_char(engine[y+1][x])) or (y != (len(engine)-1) and x != (len(engine[0])-1) and is_spec_char(engine[y+1][x+1])) \
            or (x != 0 and is_spec_char(engine[y][x-1])) or (x != (len(engine[0])-1) and is_spec_char(engine[y][x+1])):
            return True

    else:
        return False


def is_spec_char(c):
    if c in string.punctuation and c != '.':
        return True
    else:
        return False

def day2_part2(filename):
    engine = parse_file(filename)
    power = []

    for y in range(0, len(engine)):
        for x in range(0, len(engine[y])):
            if engine[y][x] == "*":
                gear_power = look_gear_around(engine, y, x)
                if gear_power is not None:
                    power.append(gear_power)
            else:
                continue

    return sum(power)

def look_gear_around(engine, y, x):
    gears = []

    # check left from *
    piece = look_left(engine, y, x-1, '')
    if len(piece) > 0:
        gears.append(piece)

    # check right from *
    piece = look_right(engine, y, x+1, '')
    if len(piece) > 0:
        gears.append(piece)

    # check down from *
    if (engine[y+1][x]).isdigit():
        piece = look_left(engine, y+1, x, '')
        piece2 = look_right(engine, y+1, x+1, '')

        gears.append(piece+piece2)
    else:
        piece = look_left(engine, y + 1, x-1, '')
        if len(piece) > 0:
            gears.append(piece)

        piece = look_right(engine, y + 1, x+1, '')
        if len(piece) > 0:
            gears.append(piece)

    # check up from *
    if (engine[y - 1][x]).isdigit():
        piece = look_left(engine, y - 1, x, '')
        piece += look_right(engine, y - 1, x + 1, '')
        gears.append(piece)
    else:
        piece = look_left(engine, y-1, x-1, '')
        if len(piece) > 0:
            gears.append(piece)

        piece = look_right(engine, y-1, x+1, '')
        if len(piece) > 0:
            gears.append(piece)

    if len(gears) == 2:
        return int(gears[0]) * int(gears[1])
    else:
        return None


def look_left(engine, y, x, number_piece):
    if 0 <= y <= len(engine)-1 and x >= 0:
        if (engine[y][x]).isdigit():
            number_piece = engine[y][x] + number_piece
            return look_left(engine, y, x-1, number_piece)
        else:
            return number_piece
    else:
        return number_piece


def look_right(engine, y, x, number_piece):
    if 0 <= y <= len(engine) - 1 and x <= len(engine[0])-1:
        if (engine[y][x]).isdigit():
            number_piece = number_piece + engine[y][x]
            return look_right(engine, y, x+1, number_piece)
        else:
            return number_piece
    else:
        return number_piece




if __name__ == '__main__':
    # print(day2_part1('inputs/day3/test_input.txt'))
    # print(day2_part1('inputs/day3/input.txt'))
    print(day2_part2('inputs/day3/input.txt'))
