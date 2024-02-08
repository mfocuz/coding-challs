#!/home/kali/Tools/mambaforge/envs/sage/bin/python
import sys
from time import sleep

from sage.combinat.debruijn_sequence import debruijn_sequence
import random

MAX_DIGITS = 65536


def vault(pin_input) -> bool:
        pin = "".join([random.choice("0123456789abcdef") for _ in range(4)])
        digits = ["z", "z", "z", "z"]
        counter = 0

        # print("What is the 4-digit PIN?")

        attempt = list(pin_input)
        while True:
            for i in range(len(attempt)):
                digits.insert(0, attempt.pop())
                digits.pop()
                if "".join(digits) == pin:
                    return True

                counter += 1
                if counter > MAX_DIGITS:
                    return False
            return False


def dumb_solution():
    full_input = ""
    for i in range(16**4):
        full_input += "{:0{n}X}".format(i, n=4)

    full_input = full_input[0:16**4]
    uniq_codes = dict()
    for c in range(len(full_input)-4):
        uniq_codes[full_input[c:c+4]] = True

    return len(uniq_codes)


def find_good_input():
    while True:
        codes = dict()
        pin = ""
        misses = 0
        while len(pin) < 65535:
            next_char = random.choice("0123456789abcdef")
            new_code = pin[-3:] + next_char
            if new_code not in codes:
                pin += next_char
                codes[new_code] = 1
            else:
                misses += 1

            if misses >= 4000000:
                break

        print("(+) Found pin input with # of %d codes, probability to hack 16 vaults is %s" % (
        len(codes), str((len(codes) / 16 ** 4) ** 16)))
        if len(codes) > 64000:
            return pin, codes


if __name__ == "__main__":
    print("(+) In case of dummy bruteforce, probability of bruteforce of 16 vaults is %s" % str(((dumb_solution() / (16 ** 4)) ** 16)))
    # pin_input, codes = find_good_input()
    pin_input = "".join([f"{i:x}" for i in debruijn_sequence(16, 4)])

    print("You've made it to vault:")
    for n in range(16):
        print(f"#{n + 1}-", end="")

        if not vault(pin_input):
            print("(-) The alarm goes off and you're forced to flee. Maybe next time!")
            sys.exit(0)
        else:
            print("OK;", end="")
            sleep(0.5)

    print("\n!!!You unlock the vault and find the flag!!!")




