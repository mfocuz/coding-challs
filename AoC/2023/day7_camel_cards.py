import sys
from collections import defaultdict

CARD_RATING = {
    "A": 12, "K": 11, "Q": 10, "J": 9, "T": 8,
    "9": 7, "8": 6, "7": 5, "6": 4, "5": 3, "4": 2, "3": 1, "2": 0
}

CARD_RATING_WITH_JOKER = {
    "A": 12, "K": 11, "Q": 10, "T": 9,
    "9": 8, "8": 7, "7": 6, "6": 5, "5": 4, "4": 3, "3": 2, "2": 1, "J": 0
}


def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    hands = dict()

    for line in lines:
        hand = line.split(' ')
        hands[hand[0]] = int(hand[1])

    return hands


def day7_part1(filename):
    hands = parse_file(filename)

    scores = defaultdict(list)
    for hand in hands:
        score = calc_hand_score(hand)
        scores[score].append(hand)

    total_score = 0
    rank = 1
    # total_hands = len(hands)
    for score in sorted(scores):
        sorted_hands = sorted(scores[score], key=sort_by_card)
        for sh in sorted_hands:
            total_score += rank * hands[sh]
            rank += 1

    return total_score


def sort_by_card(hand):
    key = [CARD_RATING[card] for card in hand]
    return key


def sort_by_card_with_joker(hand):
    key = [CARD_RATING_WITH_JOKER[card] for card in hand]
    return key


def calc_hand_score(hand):
    cards = defaultdict(int)

    jokers = 0
    hand_score = 1
    for card in hand:
        if card in cards:
            hand_score += cards[card] * hand_score

        cards[card] += 1

    return hand_score


def calc_hand_score_with_joker(hand):
    cards = defaultdict(int)

    jokers = []
    hand_score = 1
    for card in hand:
        if card == "J":
            jokers.append(card)
            continue
        elif card in cards:
            hand_score += cards[card] * hand_score
            cards[card] += 1
        else:
            cards[card] += 1

    if len(jokers) >= 4:
        # 1 + 1*1 + 2*2 + 3*6 + 4*18
        return 120

    for j in jokers:
        max_card = max(cards, key=cards.get)
        hand_score += cards[max_card] * hand_score
        cards[max_card] += 1

    return hand_score


def day7_part2(filename):
    hands = parse_file(filename)

    scores = defaultdict(list)
    for hand in hands:
        score = calc_hand_score_with_joker(hand)
        scores[score].append(hand)

    total_score = 0
    rank = 1

    for score in sorted(scores):
        sorted_hands = sorted(scores[score], key=sort_by_card_with_joker)
        for sh in sorted_hands:
            total_score += rank * hands[sh]
            rank += 1

    return total_score


if __name__ == '__main__':
    print("part1: test_input=%s" % day7_part1('inputs/day7/test_input.txt'))
    print("part1: input=%s" % day7_part1('inputs/day7/input.txt'))
    #
    print("part2: test_input=%s" % day7_part2('inputs/day7/test_input.txt'))
    print("part2: input=%s" % day7_part2('inputs/day7/input.txt'))