import re
from collections import defaultdict

def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    cards = []

    for line in lines:
        card_match = re.search('Card\s*(\d+): (.*)\|(.*)', line)
        left_numbers = [int(c) for c in card_match.group(2).split(" ") if c != '']
        right_numbers = [int(c) for c in card_match.group(3).split(" ") if c != '']
        card = [card_match.group(1), left_numbers, right_numbers]
        cards.append(card)

    return cards

def day4_part1(filename):
    cards = parse_file(filename)
    total_points = []

    for card in cards:
        matches = len(set(card[1]) & set(card[2]))
        total_points.append(2**(matches-1))

    return sum(total_points)

def day4_part2(filename):
    cards = parse_file(filename)
    collection = defaultdict(int)

    for card in cards:
        collection[int(card[0])] += 1
        score = len(set(card[1]) & set(card[2]))
        for match in range(int(card[0]) + 1, int(card[0]) + score + 1):
            collection[match] += collection[int(card[0])]

    total_cards = 0
    for card in collection:
        total_cards += collection[card]

    return total_cards


if __name__ == '__main__':
    print("part1: test_input=%s" % day4_part1('inputs/day4/test_input.txt'))
    print("part1: input=%s" % day4_part1('inputs/day4/input.txt'))

    print("part2: test_input=%s" % day4_part2('inputs/day4/test_input.txt'))
    print("part2: input=%s" % day4_part2('inputs/day4/input.txt'))
