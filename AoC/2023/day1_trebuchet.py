import re
def day1_part1():
    with open('inputs/day1/input.txt') as f:
        lines = f.read().splitlines()

    calibr_values = []
    for line in lines:
        find_values = re.search('^[A-Za-z]*(\d).*(\d)[A-Za-z]*$', line)
        if find_values is not None:
            first_value = find_values.group(1)
            last_value = find_values.group(2)
        else:
            find_single_value = re.search('^[A-Za-z]*(\d)[A-Za-z]*$', line)
            if find_single_value is not None:
                first_value = find_single_value.group(1)
                last_value = find_single_value.group(1)
            else:
                continue

        calibr_values.append(int(str(first_value) + str(last_value)))

    return sum(calibr_values)


def day1_part2():
    with open('inputs/day1/input.txt') as f:
        lines = f.read().splitlines()

    calibr_values = []
    for line in lines:
        find_values = re.search('(one|two|three|four|five|six|seven|eight|nine|zero|\d).*(one|two|three|four|five|six|seven|eight|nine|zero|\d)', line)
        if find_values is not None:
            first_value = find_values.group(1)
            last_value = find_values.group(2)
        else:
            find_single_value = re.search('(one|two|three|four|five|six|seven|eight|nine|zero|\d)', line)
            if find_single_value is not None:
                first_value = find_single_value.group(1)
                last_value = find_single_value.group(1)
            else:
                continue

        calibr_values.append(int(str(match_number(first_value)) + str(match_number(last_value))))

    return sum(calibr_values)


def match_number(number):
    mapping = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'zero': 0

    }
    if number in mapping:
        return mapping[number]
    else:
        return number


if __name__ == '__main__':
    result1 = day1_part1()
    result2 = day1_part2()
    print(result1)
    print(result2)