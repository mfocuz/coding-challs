import re


def read_file_to_structure(filename):
    blueprint_re = re.compile("Blueprint (\d+):")
    ore_re = re.compile(".*Each ore robot costs (\d+) ore.")
    clay_re = re.compile(".*Each clay robot costs (\d+) ore.")
    obsidian_re = re.compile(".*Each obsidian robot costs (\d+) ore and (\d+) clay.")
    geode_re = re.compile(".*Each geode robot costs (\d+) ore and (\d+) obsidian.")

    with open(filename) as f:
        lines = f.read().splitlines()

        blueprints = []
        blueprint_num = 0
        blueprint = {}
        for line in lines:
            if blueprint_re.match(line):
                blueprint_num = int(blueprint_re.search(line).group(1))
                blueprint = {}
            elif ore_re.match(line):
                blueprint["ore"] = ore_re.search(line).group(1)
            elif clay_re.match(line):
                blueprint["clay"] = clay_re.search(line).group(1)
            elif obsidian_re.match(line):
                blueprint["obsidian"] = {'ore': obsidian_re.search(line).group(1), 'clas': obsidian_re.search(line).group(2)}
            elif geode_re.match(line):
                blueprint["geode"] = {'ore': geode_re.search(line).group(1), 'obsidian': geode_re.search(line).group(2)}
                blueprints.append(blueprint)
            elif '' == line:
                continue
    return blueprints


def manufacture(blueprint, minutes):
    resource_ore = 0
    resource_clay = 0
    resource_obsidian = 0
    resource_geode = 0

    robot_ore = 1
    robot_clay = 0
    robot_obsidian = 0
    robot_geode = 0

    for i in range(minutes):
        if int(blueprint['ore']) <= resource_ore:
            robot_ore += 1




def task1(filename):
    blueprints = read_file_to_structure(filename)
    for i in blueprints:
        manufacture(blueprints[i], 24)

    return 1


def day19():
    test1_result = task1('inputs/day19/test.txt')
    print("%d" % test1_result)
    #
    # task1_result = task1('inputs/day19/input.txt')
    # print("%d" % task1_result)
    #
    # test2_result = task2('inputs/day19/test.txt', 2022)
    # print("%s" % test2_result)
    #
    # task2_result = task2('inputs/day19/input.txt')
    # print("%s" % task2_result)


if __name__ == '__main__':
    day19()