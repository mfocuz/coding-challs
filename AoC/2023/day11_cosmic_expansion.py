def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    y = len(lines) - 1
    universe = [[]] * (y + 1)
    for line in lines:
        row = []
        for char in line:
            row.append(char)
        universe[y] = row
        y -= 1

    return universe


def expand_universe_memory_efficient(universe):
    expanded_universe_down = dict()
    expanded_universe_right = dict()

    for i in range(len(universe)):
        if "#" not in universe[i]:
            expanded_universe_down[i] = True

    for x in range(len(universe[0])):
        no_galaxy = True
        for y in reversed(range(len(universe))):
            if universe[y][x] == "#":
                no_galaxy = False
                break

        if no_galaxy:
            expanded_universe_right[x] = True

        if x >= len(universe[0]):
            break

    return expanded_universe_down, expanded_universe_right


def find_galaxies_cool(expanded_down, expanded_right, universe, koff):
    galaxies = dict()
    galaxy_number = 1

    extended_y = 0
    for y in range(len(universe)):
        extended_x = 0
        if y in expanded_down:
            extended_y += koff
        for x in range(len(universe[y])):
            if x in expanded_right:
                extended_x += koff
            if universe[y][x] == "#":
                galaxies[galaxy_number] = [extended_x + x, extended_y + y]
                galaxy_number += 1

    return galaxies


def find_shortest_path_for_galaxy(galaxy_to_check, galaxies):
    distances = dict()
    for i in range(galaxy_to_check + 1, len(galaxies) + 1):
        if galaxies[i] == galaxies[galaxy_to_check]:
            continue

        x_diff = abs(galaxies[galaxy_to_check][0]-galaxies[i][0])
        y_diff = abs(galaxies[galaxy_to_check][1]-galaxies[i][1])

        galaxy_pair = "%d:%d" % (galaxy_to_check, i)
        distances[galaxy_pair] = (x_diff + y_diff)

    return distances


def visualize(universe):
    for y in reversed(range(len(universe))):
        line = ""
        for x in universe[y]:
            line += x
        print(line)


def day11_part1(filename):
    universe = parse_file(filename)
    expanded_universe_down, expanded_universe_right = expand_universe_memory_efficient(universe)
    # visualize(expanded_universe)

    shortest_paths = dict()
    galaxies = find_galaxies_cool(expanded_universe_down, expanded_universe_right, universe, 1)
    for galaxy in sorted(galaxies.keys()):
        distances = find_shortest_path_for_galaxy(galaxy, galaxies)
        shortest_paths.update(distances)

    return sum(shortest_paths.values())


def day11_part2(filename):
    universe = parse_file(filename)
    expanded_universe_down, expanded_universe_right = expand_universe_memory_efficient(universe)

    shortest_paths = dict()
    galaxies = find_galaxies_cool(expanded_universe_down, expanded_universe_right, universe, 999999)
    for galaxy in sorted(galaxies.keys()):
        distances = find_shortest_path_for_galaxy(galaxy, galaxies)
        shortest_paths.update(distances)

    return sum(shortest_paths.values())


if __name__ == '__main__':
    print("part1: test_input=%s" % day11_part1('inputs/day11/test_input.txt'))
    print("part1: input=%s" % day11_part1('inputs/day11/input.txt'))
    #
    print("part2: test_input=%s" % day11_part2('inputs/day11/test_input.txt'))
    print("part2: input=%s" % day11_part2('inputs/day11/input.txt'))
