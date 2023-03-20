import re

def read_packet_pairs_from_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    pairs = []
    pair = []

    for line in lines:
        if line == '':
            pairs.append(pair)
            pair = []
        else:
            p, digs = parse_line(line[1:-1])
            pair.append(digs)

    return pairs


def read_all_packets_from_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    pairs = []
    for line in lines:
        if line != '':
            skip, struct = parse_line(line)
            pairs.append(struct[0])

    return pairs


def parse_line(pair_one):
    digit = re.compile("^(\d+)[,\]$]*")
    digits = []
    while len(pair_one):
        if pair_one[0] == "[":
            pair_one = pair_one[1:]
            pair_one, values = parse_line(pair_one)
            digits.append(values)
            continue
        elif pair_one[0] == ",":
            pair_one = pair_one[1:]
            continue
        elif digit.match(pair_one):
            d = digit.match(pair_one).group(1)
            digits.append(int(d))
            pair_one = pair_one[len(d):]
            continue
        elif pair_one[0] == "]":
            return pair_one[1:], digits
    return pair_one[:], digits[:]


def compare(l, r):
    if isinstance(l, int) == isinstance(r, int) and isinstance(l, int) is True:
        if l < r:
            return True
        elif l > r:
            return False
        else:
            return None
    elif isinstance(l, int) and isinstance(r, list):
        return compare([l], r)
    elif isinstance(l, list) and isinstance(r, int):
        return compare(l, [r])
    elif isinstance(l, list) == isinstance(r, list) and isinstance(l, list) is True:
        for left, right in zip(l, r):
            result = compare(left, right)
            if result is not None:
                return result
        return compare(len(l), len(r))


def merge_sort(packets):
    if len(packets) > 1:
        m = len(packets)//2
        L = packets[:m]
        R = packets[m:]
        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if compare(L[i], R[j]):
                packets[k] = L[i]
                i += 1
            else:
                packets[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            packets[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            packets[k] = R[j]
            j += 1
            k += 1


def task1(filename):
    pairs = read_packet_pairs_from_file(filename)
    counter = 0
    for i in range(0, len(pairs)):
        result = compare(pairs[i][0], pairs[i][1])
        if result is True or result is None:
            counter += (i + 1)

    return counter


def task2(filename):
    packets = read_all_packets_from_file(filename)
    for key in ('[[2]]', '[[6]]'):
        skip, struct = parse_line(key)
        packets.append(struct[0])

    merge_sort(packets)
    code1 = 0
    code2 = 0
    for i in range(0, len(packets)):
        print(str(packets[i]))
        if str(packets[i]) == '[[2]]':
            code1 = i+1
        elif str(packets[i]) == '[[6]]':
            code2 = i+1

    return code1 * code2


def day13():
    # test1_result = task1('inputs/day13/test.txt')
    # print("%d" % test1_result)
    #
    # task1_result = task1('inputs/day13/input.txt')
    # print("%d" % task1_result)
    #
    # test2_result = task2('inputs/day13/test.txt')
    # print("%s" % test2_result)
    # #
    task2_result = task2('inputs/day13/input.txt')
    print("%s" % task2_result)


if __name__ == '__main__':
    day13()
