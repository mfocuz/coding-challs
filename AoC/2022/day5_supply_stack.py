import re


def solution_day5(lineStackNumbers):
    input_file = open('inputs/day5/input2.txt', 'r')
    lines = input_file.readlines()

    registers = {}

    registerNumber = lines[lineStackNumbers-1]
    for i in reversed(range(0, len(lines[0:lineStackNumbers])-1)):
        _regs = lines[i].strip().split(' ')
        for j in range(0, len(_regs)):
            if _regs[j] != '[_]':
                if j in registers:
                    registers[j].append(_regs[j])
                else:
                    registers[j] = [_regs[j]]

    for line in lines[int(lineStackNumbers+1):]:
        instruction_search = re.search('move\s(\d+)\sfrom\s(\d+)\sto\s(\d+)', line)
        if instruction_search:
            _move = int(instruction_search.group(1))
            _from = int(instruction_search.group(2))-1
            _to = int(instruction_search.group(3))-1

            crates = registers[_from][-_move:]
            del registers[_from][-_move:]

            for crate in crates:
                registers[_to].append(crate)


    result = ""
    for i in range(0, len(registers)):
        if len(registers[i]) > 0:
            reg = registers[i][len(registers[i])-1]
            c = re.search('\\[(\w)\\]', reg)
            if c:
                result += c.group(1)

    print(result)



if __name__ == '__main__':
    solution_day5(9)