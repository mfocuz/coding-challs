import re
from collections import defaultdict

map_order = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location"
]

def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    seed_map = dict()

    seeds = []
    state = "START"
    for line in lines:
        if re.match("seeds:(.*)", line):
            s = re.search("seeds: (.*)", line)
            seeds = [int(x) for x in s.group(1).split(' ')]
            continue
        elif len(line) == 0:
            continue
        elif re.match(".* map:.*", line):
            s = re.search("(.*) map:.*", line)
            state = s.group(1)
            continue

        if state not in seed_map:
            seed_map[state] = []

        mapping = line.split()
        seed_map[state].append([int(x) for x in mapping])

    return seeds, seed_map


def day5_part1(filename):
    seeds, seed_map = parse_file(filename)

    min_location = None
    for seed in seeds:
        location = find_location(seed, seed_map)
        if min_location is None or min_location > location:
            min_location = location

    return min_location


def find_location(seed, seed_map):
     for map_type in map_order:
         for mapping in seed_map[map_type]:
             dest = mapping[0]
             src = mapping[1]
             seed_range = mapping[2]
             if src <= seed <= src + seed_range:
                seed = dest + (seed - src)
                break
             else:
                continue

     return seed


def day5_part2(filename):
    seeds, seed_map = parse_file(filename)

    seed_pairs = [(seeds[i], seeds[i] + seeds[i+1]) for i in range(0, len(seeds)-1, 2)]

    min_location = None
    for seed_pair in seed_pairs:

        location = range_mapper(seed_pair, seed_map, 0)
        if min_location is None or min_location > location:
            min_location = location

    return min_location

    return 0





def day5_part2(filename):
    seeds, seed_map = parse_file(filename)

    seed_pairs = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds)-1, 2)]
    print("Approx time estimation=%d" % brute_time_estimation(seed_pairs))

    min_location = None
    for seed_pair in seed_pairs:
        print("Checking seed pair %d-%d" % (seed_pair[0], seed_pair[1]))
        for seed in range(seed_pair[0], seed_pair[0] + seed_pair[1] + 1):
            if seed % 1000000 == 0:
                print("checking seed=%d" % seed)
            location = find_location(seed, seed_map)
            if min_location is None or min_location > location:
                min_location = location

    return min_location

    return 0


def brute_time_estimation(seed_pairs):
    total = 0
    for pair in seed_pairs:
        total = total + (pair[1]/1000000)

    return total


def find_location_with_range(seed_pair, seed_map):
    seed_low = seed_pair[0]
    seed_top = seed_pair[0] + seed_pair[1]
    seed = seed_low
    for map_type in map_order:
        for mapping in seed_map[map_type]:
            dest = mapping[0]
            src = mapping[1]
            seed_range = mapping[2]
            if src <= seed_low <= src + seed_range:
                seed = dest + (seed_low - src)
                break
            elif src <= seed_top <= src + seed_range:
                seed = dest + (seed_top - src)
            else:
                continue

    return seed


if __name__ == '__main__':
    # print("part1: test_input=%s" % day5_part1('inputs/day5/input_test.txt'))
    # print("part1: input=%s" % day5_part1('inputs/day5/input.txt'))
    #
    print("part2: test_input=%s" % day5_part2('inputs/day5/input_test.txt'))
    print("part2: input=%s" % day5_part2('inputs/day5/input.txt'))
