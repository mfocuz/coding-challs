def task_1():
    with open('inputs/day2/input.txt') as f:
        lines = f.read().splitlines()

    result_map = {
        'AX': 'D', 'BX': 'L', 'CX': 'W',
        'AY': 'W', 'BY': 'D', 'CY': 'L',
        'AZ': 'L', 'BZ': 'W', 'CZ': 'D'
    }
    shape_map = {'X': 'R', 'Y': 'P', 'Z': 'S'}

    my_score = 0
    for line in lines:
        strategy = line.split(' ')
        opponent = strategy[0]
        myself = strategy[1]
        result = result_map[opponent + myself]
        my_score += calc_score(result, shape_map[myself])
    print("task1=%d" % my_score)


def task_2():
    with open('inputs/day2/input.txt') as f:
        lines = f.read().splitlines()

    my_score = 0
    for line in lines:
        strategy = line.split(' ')
        opponent = strategy[0]
        result = strategy[1]

        choose_shape = {
            'AX': 'S', 'BX': 'R', 'CX': 'P',
            'AY': 'R', 'BY': 'P', 'CY': 'S',
            'AZ': 'P', 'BZ': 'S', 'CZ': 'R'
        }
        result_map = {'X': 'L', 'Y': 'D', 'Z': 'W'}

        my_score += calc_score(result_map[result], choose_shape[opponent+result])
    print("task2=%d" % my_score)


def calc_score(result, shape):
    score_game_map = {'W': 6, 'D': 3, 'L': 0}
    score_shape_map = {'R': 1, 'P': 2, 'S': 3}
    score = score_game_map[result] + score_shape_map[shape]
    return score


def day2():
    task_1()
    task_2()


if __name__ == '__main__':
    day2()