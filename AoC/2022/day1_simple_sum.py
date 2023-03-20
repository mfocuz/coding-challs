def day1():
    with open('inputs/day1/input.txt') as f:
        lines = f.read().splitlines()

    current_elf_carr = 0
    elfs = []
    for line in lines:
        if line == "":
            elfs.append(current_elf_carr)
            current_elf_carr = 0
        else:
            current_elf_carr += int(line)

    elfs.sort(reverse=True)
    print("task1=%d" % elfs[0])
    print("task2=%d" % (elfs[0] + elfs[1] + elfs[2]))


if __name__ == '__main__':
    day1()