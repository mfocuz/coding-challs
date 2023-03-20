import re


def read_input_to_structure(filename):
    input_file = open(filename, 'r')
    lines = input_file.readlines()
    moves = []
    for move in (lines):
        parse = re.search("(\w)\s(\d+)", move)
        direction = parse.group(1)
        steps = int(parse.group(2))
        moves.append([direction, steps])

    return moves


def move_rope(filename, rope_length, to_viz):
    moves = read_input_to_structure(filename)
    board_x = [0, 0]
    board_y = [0, 0]
    rope = [[0, 0] for y in range(rope_length)]
    uniq_tail_pos = {"x=0;y=0": 1}

    if to_viz:
        visualize(board_x, board_y, rope)

    for move in moves:
        for step in range(0, move[1]):
            if move[0] == "R":
                rope[0][0] += 1
            elif move[0] == "L":
                rope[0][0] -= 1
            elif move[0] == "U":
                rope[0][1] += 1
            elif move[0] == "D":
                rope[0][1] -= 1

            board_x, board_y = recalc_board(board_x, board_y, rope[0])
            knot_moved, rope = move_knot(rope)
            tail_uniq = "x=%d;y=%d" % (rope[rope_length-1][0], rope[rope_length-1][1])
            if tail_uniq not in uniq_tail_pos:
                uniq_tail_pos[tail_uniq] = 1

            if to_viz:
                visualize(board_x, board_y, rope)

    return len(uniq_tail_pos)


def move_knot(rope):
    is_moved = False
    sign = lambda a: (a >> 127) | (not not a)
    for i in range(1, len(rope)):
        dx = rope[i-1][0] - rope[i][0]
        dy = rope[i-1][1] - rope[i][1]
        if abs(dx) > 1 or abs(dy) > 1:
            is_moved = True
            rope[i][0] += sign(dx)
            rope[i][1] += sign(dy)

    return is_moved, rope,


def recalc_board(board_x, board_y, head):
    if head[0] < 0:
        if board_x[0] > head[0]:
            board_x[0] = head[0]
    else:
        if board_x[1] < head[0]:
            board_x[1] = head[0]

    if head[1] < 0:
        if board_y[0] > head[1]:
            board_y[0] = head[1]
    else:
        if board_y[1] < head[1]:
            board_y[1] = head[1]

    return board_x, board_y


def visualize(board_x, board_y, rope):
    for i in reversed(range(board_y[0], board_y[1] + 1)):
        line = ""
        for j in range(board_x[0], board_x[1] + 1):
            position = "."
            for k in range(0, len(rope)):
                if k == 0:
                    knot_name = "H"
                else:
                    knot_name = str(k)

                if j == rope[k][0] and i == rope[k][1]:
                    position = knot_name
                    break
            line += position
        print(line)
    print("\r")


if __name__ == '__main__':
    test_result = move_rope('inputs/day9/test.txt', 2, False)
    print("Answer(test)=%d; expected 13" % test_result)

    test_result = move_rope('inputs/day9/test.txt', 10, False)
    print("Answer(test)=%d; expected 1" % test_result)

    task1_result = move_rope('inputs/day9/input.txt', 2, False)
    print("Answer(task1)=%d;" % task1_result)

    test_result = move_rope('inputs/day9/test2.txt', 10, False)
    print("Answer(test2)=%d; expected 36" % test_result)

    task2_result = move_rope('inputs/day9/input.txt', 10, False)
    print("Answer(task2)=%d" % task2_result)