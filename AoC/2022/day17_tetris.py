def read_file_to_structure(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    moves = []
    for line in lines:
        for i in line:
            moves.append(i)
    return moves


def rock_fall(rock, tunnel):
    if tunnel.is_connected(rock):
        return 'Stop'
    for piece in rock:
        piece[1] -= 1
    return rock


def push_rock(rock, direction, tunnel):
    push_mapping = {'<': -1, '>': +1}
    new_rock_position = []
    for part in rock:
        i, j = part[0], part[1]
        i += push_mapping[direction]
        if i < 0 or i > 6 or tunnel.state[j][i] == '#':
            return rock
        else:
            new_rock_position.append([i, j])

    return new_rock_position


def rock_generator():
    state = 0
    types = 5

    def generator(higher_point):
        nonlocal state
        # |rock:
        # |####
        if state == 0:
            rock = [[2, 0], [3, 0], [4, 0], [5, 0]]
        # |rock
        # |.#.
        # |###
        # |.#.
        elif state == 1:
            rock = [[3, 0], [2, 1], [3, 1], [4, 1], [3, 2]]
        # |rock
        # |..#
        # |..#
        # |###
        elif state == 2:
            rock = [[2, 0], [3, 0], [4, 0], [4, 1], [4, 2]]
        # |rock
        # |#
        # |#
        # |#
        # |#
        elif state == 3:
            rock = [[2, 0], [2, 1], [2, 2], [2, 3]]
        # |rock
        # |##
        # |##
        elif state == 4:
            rock = [[2, 0], [3, 0], [2, 1], [3, 1]]

        state = (state + 1) % types
        for piece in rock:
            piece[1] += higher_point
        return rock

    return generator


class Tunnel:
    tunnel_width = 7
    tunnel_peek = -1
    state = None

    def __init__(self):
        self.state = []
        for j in range(self.tunnel_peek + 5):
            row = []
            for i in range(self.tunnel_width):
                row.append('.')
            self.state.append(row)

    def update(self, new_rock):
        highest_point = self.tunnel_peek
        for piece in new_rock:
            self.state[piece[1]][piece[0]] = '#'
            if (piece[1]+1 + 3) > highest_point:
                highest_point = piece[1]

        if highest_point > self.tunnel_peek:
            for i in range(highest_point - self.tunnel_peek + 3):
                self.state.append(['.'] * self.tunnel_width)
            self.tunnel_peek = highest_point

    def is_connected(self, rock):
        for piece in rock:
            if self.state[piece[1]-1][piece[0]] == '#' or piece[1] == 0:
                return True
        return False


    def get_state(self):
        return self.state

    def get_height(self):
        return self.tunnel_peek


def visualize(tunnel, next_rock):
    for j in reversed(range(tunnel.get_height()+5)):
        line = ""
        for i in range(7):
            is_next_rock = False
            for piece in next_rock:
                if piece[1] == j and piece[0] == i:
                    is_next_rock = True
                    break
            if is_next_rock:
                line += '@'
            else:
                line += tunnel.state[j][i]
        print("|%s|" % line)
    print("+-------+")


def play_tetris(moves, iterations):
    move_pointer = 0
    rock_gen = rock_generator()
    tunnel = Tunnel()
    iteration = -1
    for i in range(iterations):
        next_rock = rock_gen(tunnel.get_height() + 4)
        while True:
            # visualize(tunnel, next_rock)
            iteration += 1
            if iteration % 2 == 1:
                next_rock_save = next_rock.copy()
                next_rock = rock_fall(next_rock, tunnel)
                if next_rock == 'Stop':
                    tunnel.update(next_rock_save)
                    break
            else:
                next_rock = push_rock(next_rock, moves[move_pointer], tunnel)
                move_pointer = (move_pointer + 1) % len(moves)

    return tunnel


def task1(filename):
    moves = read_file_to_structure(filename)
    tunnel = play_tetris(moves, 2022)

    return tunnel.get_height() + 1


def task2(filename, iterations):
    moves = read_file_to_structure(filename)
    tunnel = play_tetris(moves, len(moves))

    cycles = iterations / len(moves)
    result = cycles * tunnel.get_height()

    return result


def day16():
    # test1_result = task1('inputs/day17/test.txt')
    # print("%d" % test1_result)
    #
    # task1_result = task1('inputs/day17/input.txt')
    # print("%d" % task1_result)
    #
    test2_result = task2('inputs/day17/test.txt', 2022)
    print("%s" % test2_result)
    #
    # task2_result = task2('inputs/day16/input.txt')
    # print("%s" % task2_result)


if __name__ == '__main__':
    day16()
