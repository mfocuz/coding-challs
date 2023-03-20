def task1():
    input_file = open('inputs/day3/input.txt', 'r')
    elfs = []

    lines = input_file.readlines()
    priority_sum = 0
    for line in lines:
        line = line.rstrip()
        m = int(len(line)/2)
        p1 = line[:m]
        p2 = line[m:]
        print("len p1=%d, p2=%s" % (len(p1), len(p2)))

        p1_dict = convert(p1)
        p2_dict = convert(p2)

        for i in p1_dict:
            if i in p2_dict:
                priority_sum += calc_priority(i)

    print("Answer=%d" % priority_sum)


def solution_day3_2():
    input_file = open('inputs/day3/input.txt', 'r')

    lines = input_file.readlines()
    priority_sum = 0
    for index in range(0, len(lines), 3):
        e1 = lines[index].rstrip()
        e2 = lines[index+1].rstrip()
        e3 = lines[index+2].rstrip()

        p1_dict = convert(e1)
        p2_dict = convert(e2)
        p3_dict = convert(e3)

        for i in p1_dict:
            if i in p2_dict and i in p3_dict:
                priority_sum += calc_priority(i)

    print("Answer=%d" % priority_sum)


def calc_priority(item):
    items = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return (items.index(item) + 1)


def convert(arr):
    d = dict()
    for i in arr:
        d[i] = 1
    return d


def day3():
    task1()


if __name__ == '__main__':
    day3()