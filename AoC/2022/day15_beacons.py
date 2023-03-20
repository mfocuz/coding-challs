import re
from intervaltree import Interval, IntervalTree


def create_field(search_range):
    field = [None for x in range(search_range)]

    def distress_field(y, xl=None, xr=None):
        if field[y] is None:
            field[y] = IntervalTree()

        if xl == xr is None:
            field[y].merge_overlaps()
            return field[y]

        interval = Interval(xl, xr + 1, (xl, xr + 1))
        field[y].add(interval)
        return field[y]

    return distress_field


def read_file_to_structure(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    pattern = re.compile("Sensor at x=(-?\d+), y=(\d+): closest beacon is at x=(-?\d+), y=(\d+)")
    pairs = dict()
    for line in lines:
        if pattern.match(line):
            m = pattern.match(line)
            x1, y1, x2, y2 = m.group(1), m.group(2), m.group(3), m.group(4)
            pairs["%s:%s" % (x1, y1)] = "%s:%s" % (x2, y2)
    return pairs


def mark_field_scanned(distress_field, sensor_x, sensor_y, beacon_x, beacon_y, target_y):
    distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

    if abs(target_y - sensor_y) > distance:
        return

    target_row_length_half = distance - abs(target_y - sensor_y)
    target_x1 = sensor_x - target_row_length_half
    target_x2 = sensor_x + target_row_length_half
    distress_field(target_y, target_x1, target_x2)


def task1(filename, target_y):
    pairs = read_file_to_structure(filename)

    target_row = target_y
    distress_field = create_field(target_row + 1)
    for key in pairs:
        s_x, s_y = [int(k) for k in key.split(':')]
        b_x, b_y = [int(k) for k in pairs[key].split(':')]

        mark_field_scanned(distress_field, s_x, s_y, b_x, b_y, target_y)

    result = 0
    for interval in distress_field(target_row):
        result += interval.end - interval.begin

    return result-1


def task2(filename, search_range):
    pairs = read_file_to_structure(filename)

    distress_field = create_field(search_range * 2 + 1)
    for key in pairs:
        sensor_x, sensor_y = [int(k) for k in key.split(':')]
        beacon_x, beacon_y = [int(k) for k in pairs[key].split(':')]
        distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        #print("sonar %d:%d, beacon %d:%d" % (sensor_x, sensor_y, beacon_x, beacon_y))
        for i in range(sensor_y - distance, sensor_y + distance):
            mark_field_scanned(distress_field, sensor_x, sensor_y, beacon_x, beacon_y, i)

    for i in range(search_range + 1):
        intervals = []
        for interval in distress_field(i):
            intervals.append([interval.begin, interval.end])

        if len(intervals) > 1 and (sorted(intervals)[1][0] - sorted(intervals)[0][1]) > 0:
            print("y=%d, x=%s" % (i, sorted(intervals)[0][1]))
            result = sorted(intervals)[0][1] * 4000000 + i
            return result

    return 0


def day15():
    test1_result = task1('inputs/day15/test.txt', 10)
    print("%d" % test1_result)
    #
    task1_result = task1('inputs/day15/input.txt', 2000000)
    print("%d" % task1_result)

    test2_result = task2('inputs/day15/test.txt', 20)
    print("%s" % test2_result)
    # this one is very slow, ~10 mins
    # task2_result = task2('inputs/day15/input.txt', 4000000)
    # print("frequency=%d" % task2_result)


if __name__ == '__main__':
    day15()
