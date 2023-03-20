import math
import re


def parse_monkeys(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    is_new_monkey = re.compile("Monkey\s(\d+)*")
    start_items = re.compile("\s*Starting items:\s(.*)")
    operation = re.compile("\s*Operation: new = old (.*)")
    test = re.compile("\s*Test: divisible by (\d+)")
    if_true = re.compile("\s*If true: throw to monkey\s(\d+)")
    if_false = re.compile("\s*If false: throw to monkey\s(\d+)")

    monkeys = []
    monkey = None
    for line in lines:
        if is_new_monkey.match(line):
            monkey = {}
            monkey_num = is_new_monkey.search(line).group(1)
            continue

        elif start_items.match(line):
            items = [int(x) for x in start_items.search(line).group(1).split(",")]
            monkey["items"] = items
            continue

        elif operation.match(line):
            operation_parse = re.search("([+\-*/])\s([\w\d]*)", line)
            monkey["operation"] = {"op": operation_parse.group(1), "term": operation_parse.group(2)}

        elif test.match(line):
            monkey["div"] = int(test.search(line).group(1))

        elif if_true.match(line):
            monkey["true"] = int(if_true.search(line).group(1))

        elif if_false.match(line):
            monkey["false"] = int(if_false.search(line).group(1))
            monkey["counter"] = 0
            monkeys.append(monkey)

    return monkeys


def task1(filename):
    monkeys = parse_monkeys(filename)

    def do_round(monkeys):
        for monkey in monkeys:
            items = monkey["items"].copy()
            for item in monkey["items"]:
                worry_lvl = math.floor(op(item, monkey["operation"]) / 3)
                del (items[0])
                monkey["counter"] += 1
                if worry_lvl % monkey["div"] == 0:
                    monkeys[monkey["true"]]["items"].append(worry_lvl)
                else:
                    monkeys[monkey["false"]]["items"].append(worry_lvl)
            monkey["items"] = items

        return monkeys

    for i in range(0, 20):
        monkeys = do_round(monkeys)

    counters = sorted([monkey["counter"] for monkey in monkeys])

    return counters[len(counters)-1] * counters[len(counters)-2]


def task2(filename):
    monkeys = parse_monkeys(filename)

    modulus = 1
    for monkey in monkeys:
        modulus *= monkey["div"]

    for i in range(0, 10000):
        monkeys = do_round(monkeys, modulus)
        print("round=%d" % i)
        #[print("counter=%d;" % monkeys[i]["counter"]) for i in range(0, len(monkeys))]

    counters = sorted([monkey["counter"] for monkey in monkeys])

    return counters[len(counters)-1] * counters[len(counters)-2]


def do_round(monkeys, modulus):
    for monkey in monkeys:
        items = monkey["items"].copy()
        for item in monkey["items"]:
            worry_lvl = math.floor(op(item, monkey["operation"])) % modulus
            del (items[0])
            monkey["counter"] += 1
            if worry_lvl % monkey["div"] == 0:
                monkeys[monkey["true"]]["items"].append(worry_lvl)
            else:
                monkeys[monkey["false"]]["items"].append(worry_lvl)
        monkey["items"] = items

    return monkeys


def op(term1, operation):
    term1 = int(term1)
    if operation["term"] == "old":
        term2 = term1
    else:
        term2 = int(operation["term"])

    if operation["op"] == "*":
        return term1 * term2
    elif operation["op"] == "/":
        return term1 / term2
    elif operation["op"] == "+":
        return term1 + term2
    elif operation["op"] == "-":
        return term1 - term2


def day11():
    # test1_result = task1('inputs/day11/test.txt')
    # print("%s" % test1_result)

    # task1_result = task1('inputs/day11/input.txt')
    # print("%s" % task1_result)

    # test2_result = task2('inputs/day11/test.txt')
    # print("%s" % test2_result)

    task2_result = task2('inputs/day11/input.txt')
    print("%s" % task2_result)


if __name__ == '__main__':
    day11()