import re


def task1(filename, cpu_inst):
    with open(filename) as f:
        lines = f.read().splitlines()

    search_c = [20, 60, 100, 140, 180, 220]
    signal = 0
    for line in lines:
        while True:
            reg_x, cycles, instr_exec = cpu_inst(line)
            if cycles+1 in search_c:
                print("c=%d;x=%d" % (cycles, reg_x))
                signal += reg_x * (cycles+1)

            if instr_exec == 0:
                break
            else:
                continue

    return signal


def task2(filename, cpu_inst):
    with open(filename) as f:
        lines = f.read().splitlines()

    crt_pos = 0
    crt_line = ""
    reg_x, cycles, instr_exec = cpu_inst("noop")
    for line in lines:
        while True:
            if crt_pos == 40:
                crt_pos = 0
                crt_line += "\n"

            if reg_x-1 <= crt_pos <= reg_x+1:
                crt_line += "#"
            else:
                crt_line += "."

            reg_x, cycles, instr_exec = cpu_inst(line)
            crt_pos += 1
            if instr_exec == 0:
                break
            else:
                continue
    return crt_line


def cpu():
    reg_x = 1
    cycles = 0
    instr_exec = 0

    def run_cycle(input_line):
        nonlocal cycles, reg_x, instr_exec

        if "noop" in input_line:
            cycles += 1
        else:
            instruction_parse = re.search("(\\w+)\\s(-?\\d*)", input_line)
            instruction = instruction_parse.group(1)
            value = instruction_parse.group(2)

            instr_exec += 1
            cycles += 1

            if instr_exec == 2:
                instr_exec = 0
                reg_x += int(value)

        return reg_x, cycles, instr_exec
    return run_cycle


def day10():
    #cpu_inst = cpu(1)
    # test1_result = task1('inputs/day10/test.txt', cpu_inst)
    # print("test1=%d" % test1_result)

    # cpu_inst = cpu(1)
    # task1_result = task1('inputs/day10/input.txt', cpu_inst)
    # print("test1=%d" % task1_result)

    # cpu_inst = cpu()
    # test2_result = task2('inputs/day10/test.txt', cpu_inst)
    # print("%s" % test2_result)

    cpu_inst = cpu()
    task2_result = task2('inputs/day10/input.txt', cpu_inst)
    print("%s" % task2_result)


if __name__ == '__main__':
    day10()
