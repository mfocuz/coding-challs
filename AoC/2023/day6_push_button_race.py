import re


def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    time_parse = re.search("Time:\s*(\d*.*)", lines[0])
    distance_parse = re.search("Distance:\s*(\d*.*)", lines[1])

    times = [int(x) for x in time_parse.group(1).split(' ') if len(x) > 0]
    distances = [int (x) for x in distance_parse.group(1).split(' ') if len(x) > 0]

    return times, distances

def day6_part1(filename):
    times, distances = parse_file(filename)
    winners = find_winners(times, distances)

    return winners


def find_winners(times, distances):
    winners = []
    for race_i in range(0, len(times)):
        win_push_time_left = None
        for push_time in range(0, times[race_i]):
            if push_time * (times[race_i] - push_time) > distances[race_i]:
                win_push_time_left = push_time
                break

        winners.append(times[race_i] - win_push_time_left * 2 + 1)

    return multiply_array_elements(winners)


def multiply_array_elements(arr):
    result = 1
    for element in arr:
        result *= element
    return result


def day6_part2(filename):
    times, distances = parse_file(filename)
    times = [str(x) for x in times]
    total_time = "".join(times)

    distances = [str(x) for x in distances]
    total_dist = "".join(distances)

    winners = find_winners([int(total_time)], [int(total_dist)])

    return winners


if __name__ == '__main__':
    print("part1: test_input=%s" % day6_part1('inputs/day6/test_input.txt'))
    print("part1: input=%s" % day6_part1('inputs/day6/input.txt'))
    #
    print("part2: test_input=%s" % day6_part2('inputs/day6/test_input.txt'))
    print("part2: input=%s" % day6_part2('inputs/day6/input.txt'))
