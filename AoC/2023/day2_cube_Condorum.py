import re
def day2_part1():
    with open('inputs/day2/input.txt') as f:
        lines = f.read().splitlines()

    conditions = {
        'red': 12,
        'green': 13,
        'blue': 14
    }

    possible_games_count = []
    for line in lines:
        game_data_string = re.search('Game\s(\d+): (.*)', line)
        game_num = game_data_string.group(1)
        game_data = game_data_string.group(2)

        game_iterations = game_data.split(';')

        if check_if_possible(game_iterations, conditions):
            possible_games_count.append(int(game_num))
        else:
            continue

    return sum(possible_games_count)


def check_if_possible(game_iterations, conditions):
    for iteration in game_iterations:
        cubes = iteration.split(',')
        for cube in cubes:
            cube_data = re.search('(\d+)\s([a-z]*)', cube)
            qt = cube_data.group(1)
            color = cube_data.group(2)

            if int(qt) > conditions[color]:
                return False

    return True


def day2_part2():
    with open('inputs/day2/input.txt') as f:
        lines = f.read().splitlines()

    powers = []
    for line in lines:
        game_data_string = re.search('Game\s(\d+): (.*)', line)
        game_num = game_data_string.group(1)
        game_data = game_data_string.group(2)

        game_iterations = game_data.split(';')

        power = find_min_qt_cubes(game_iterations)
        powers.append(power)

    return sum(powers)


def find_min_qt_cubes(game_iterations):
    qubes_min_qt = {
        'red': 0,
        'green': 0,
        'blue': 0
    }
    for iteration in game_iterations:
        cubes = iteration.split(',')
        for cube in cubes:
            cube_data = re.search('(\d+)\s([a-z]*)', cube)
            qt = int(cube_data.group(1))
            color = cube_data.group(2)

            if qt > qubes_min_qt[color]:
                qubes_min_qt[color] = qt

    return qubes_min_qt['red'] * qubes_min_qt['green'] * qubes_min_qt['blue']


if __name__ == '__main__':
    result1 = day2_part1()
    result2 = day2_part2()
    print(result1)
    print(result2)