import re


def read_file_input(filepath):
    input_file = open(filepath, 'r')
    fs = {}

    lines = input_file.readlines()
    parse_history(lines, 0, fs)

    return fs


def parse_history(lines, index, fs):
    while True:
        if index == len(lines):
            #print("index reached! = %d" % index)
            return index
        cmd_line = lines[index].rstrip()
        if not cmd_line.startswith('$'):
            print("smth goes wrong")
            exit - 1

        cmd_parse = re.search("^\$\s*(\w*)\s*([\w+\/\.]*)", cmd_line)
        cmd = cmd_parse.group(1)
        path = cmd_parse.group(2)
        index += 1

        if cmd == 'cd':
            #print("change dir to %s" % path)
            if path == "..":
                return index
            else:
                fs[path] = {}
                index = parse_history(lines, index, fs[path])
        elif cmd == 'ls':
            content, index = list_dir(lines, index)
            for entry in content:
                if "dir" not in entry:
                    entry_parser = re.search("(\d*)\s(.*)", entry)
                    size = entry_parser.group(1)
                    file_name = entry_parser.group(2)
                    fs[file_name] = size


def list_dir(lines, index):
    content = []
    while True:
        if index < len(lines):
            check_end_of_output = re.search("^\$", lines[index])
            if check_end_of_output:
                return content, index
            else:
                output_line = lines[index].rstrip()
                content.append(output_line)
                index += 1
        else:
            print("end of file, we done")
            return content, index


def calc_file_sizes(fs, size, cb):
    for key in fs:
        if isinstance(fs[key], str):
            size += int(fs[key])
        else:
            dir_size = calc_file_sizes(fs[key], 0, cb)
            if (cb != None):
                cb(dir_size)
            size += dir_size

    return size


def cb_find_dir_to_delete(to_free):
    candidate_size = 300000000
    def do(size):
        nonlocal candidate_size
        if (size > to_free and size < candidate_size):
            candidate_size = size

        return candidate_size

    return do


def cb_100k_cond():
    total = 0

    def do(a):
        if a < 100_000:
            nonlocal total
            total += a
            return total

    return do


if __name__ == '__main__':
    # #solve my test.txt file
    # cb100kmytest = cb_100k_cond()
    # fs = read_file_input('mytest.txt')
    # size = calc_file_sizes(fs, 0, cb100kmytest)
    # print("total file size(mytest)=%d (should be 38)" % size)
    #
    # # solve test.txt file
    # cb100ktest = cb_100k_cond()
    # fs = read_file_input('test.txt.txt')
    # size = calc_file_sizes(fs, 0, cb100ktest)
    # print("total file size(test.txt)=%d (should be 48381165)" % size)
    # print("answer=%d" % cb100ktest(0))
    #
    #
    # # solve challenge, p1
    # cb100kp1 = cb_100k_cond()
    # fs = read_file_input('input.txt')
    # input_total_size = calc_file_sizes(fs, 0, cb100kp1)
    # print("total file size(input)=%d (should be 44804833)" % size)
    # print("answer p1=%d" % cb100kp1(0))

    # solve chall, p2, test.txt
    fs = read_file_input('inputs/day7/test.txt')
    input_total_size = calc_file_sizes(fs, 0, None)
    to_free = 30000000 - (70000000 - input_total_size)
    print("to_free=%d" % to_free)
    cb_find_dir = cb_find_dir_to_delete(to_free)
    calc_file_sizes(fs, 0, cb_find_dir)

    print("answer=%d" % cb_find_dir(0))

    # solve p2 chall
    fs = read_file_input('inputs/day7/input.txt')
    input_total_size = calc_file_sizes(fs, 0, None)
    to_free = 30000000 - (70000000 - input_total_size)
    print("to_free=%d" % to_free)
    cb_find_dir = cb_find_dir_to_delete(to_free)
    calc_file_sizes(fs, 0, cb_find_dir)

    print("answer=%d" % cb_find_dir(0))
