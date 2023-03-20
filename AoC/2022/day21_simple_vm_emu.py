import re
import sys


def read_file_to_structure(filename, key=1):
    with open(filename) as f:
        lines = f.read().splitlines()

    constant_re = re.compile('(\w+):\s(\d+)')
    operation_re = re.compile('(\w+):\s(\w+)\s([+\-*/])\s(\w+)')
    text = dict()
    stack = list()
    for line in lines:
        if constant_re.match(line):
            text[constant_re.search(line).group(1)] = int(constant_re.search(line).group(2))
            stack.append(constant_re.search(line).group(1))
        elif operation_re.match(line):
            text[operation_re.search(line).group(1)] = {operation_re.search(line).group(3): [operation_re.search(line).group(2), operation_re.search(line).group(4)]}
            stack.append(operation_re.search(line).group(1))
        else:
            print("parsing doesn't work")
            sys.exit(0)

    return text, stack


def perform_operation(op1, op2, operation):
    if operation == "+":
        return op1 + op2
    elif operation == "-":
        return op1 - op2
    elif operation == "*":
        return op1 * op2
    elif operation == "/":
        return int(op1 / op2)


def emulate_vm(text, stack):
    ip = 0
    while len(stack) != 0:
        if ip >= len(stack):
            ip = ip % len(stack)

        if isinstance(text[stack[ip]], int):
            del stack[ip]
        elif isinstance(text[stack[ip]], dict):
            operation = list(text[stack[ip]].keys())[0]
            operand1, operand2 = text[stack[ip]][operation]

            if isinstance(operand1, str) and isinstance(text[operand1], int):
                operand1 = text[operand1]
            if isinstance(operand2, str) and isinstance(text[operand2], int):
                operand2 = text[operand2]

            if isinstance(operand1, int) and isinstance(operand2, int):
                text[stack[ip]] = perform_operation(operand1, operand2, operation)
                del stack[ip]
            ip += 1

        else:
            print("KERNEL PANIC")
            sys.exit(-1)
    return text


# def find_stack_trace(text, ast, current_func, target_func):
#     if current_func == target_func or isinstance(text[current_func], int):
#         ast[current_func] = text[current_func]
#         return ast
#     elif isinstance(text[current_func], dict):
#         left = list(dict(text[current_func]).values())[0][0]
#         right = list(dict(text[current_func]).values())[0][1]
#         find_stack_trace(text, ast, left, target_func)
#         find_stack_trace(text, ast, right, target_func)


def task1(filename):
    text, stack = read_file_to_structure(filename)
    text = emulate_vm(text, stack)

    return text["root"]


def task2(filename):
    text, stack = read_file_to_structure(filename)


    # extract root first
    root_op1, root_op2 = list(text["root"].values())[0]
    first_exec = emulate_vm(text.copy(), stack.copy())
    diff = first_exec[root_op2] - first_exec[root_op1]
    del stack[0]
    myself = "humn"
    text[myself] += 10

    # a bit cheating solution with binary search, but it is a solution!
    while True:
        new_exec = emulate_vm(text.copy(), stack.copy())
        new_diff = new_exec[root_op2] - new_exec[root_op1]
        if new_diff > diff:
            text[myself] = text[myself]//2
        elif new_diff < diff:
            text[myself] = text[myself] * 2
        elif new_diff == 0:
            break


    return text[myself]


def day21():
    # test1_result = task1('inputs/day21/test.txt')
    # print("result=%d" % test1_result)
    #
    # task1_result = task1('inputs/day21/input.txt')
    # print("%d" % task1_result)
    #
    test2_result = task2('inputs/day21/test.txt')
    print("%s" % test2_result)
    #
    # task2_result = task2('inputs/day21/input.txt')
    # print("%s" % task2_result)


if __name__ == '__main__':
    day21()