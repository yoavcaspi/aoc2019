from __future__ import annotations
import argparse
import sys
from collections import defaultdict
from typing import List, Dict, Tuple, Set


def cut(deck: List[int], num: int) -> List[int]:
    return deck[num:] + deck[:num]


def deal_into_new_stack(deck: List[int]) -> List[int]:
    return deck[::-1]


def deal_with_increment(deck: List[int], num: int) -> List[int]:
    new_deck = [-1] * len(deck)
    for i in range(len(deck)):
        j = (i * num) % len(deck)
        new_deck[j] = deck[i]
    return new_deck


def sol1(data: str, size: int = 10_007) -> int:
    deck = list(range(size))
    for line in data.splitlines():
        if line.startswith("cut"):
            num = int(line.split(" ")[-1])
            deck = cut(deck, num)
        elif line.startswith("deal with increment"):
            num = int(line.split(" ")[-1])
            deck = deal_with_increment(deck, num)
        else:
            assert line == "deal into new stack"
            deck = deal_into_new_stack(deck)
    # return " ".join([str(card) for card in deck])
    return deck.index(2019)


def cut2(deck_size: int, current_pos: int, num: int) -> int:
    return (current_pos + num) % deck_size


def deal_into_new_stack2(deck_size: int, current_pos: int) -> int:
    return deck_size - current_pos


def deal_with_increment2(deck_size: int, current_pos: int, num: int) -> int:
    # div, mod = divmod(current_pos, num)
    # return (num * mod - div) % deck_size
    return (num * current_pos) % deck_size


def sol2(data: str, size: int = 10_007, pos: int = 2019) -> int:
    deck = list(range(size))
    new_pos = pos
    for line in data.splitlines():
        if line.startswith("cut"):
            num = int(line.split(" ")[-1])
            deck = cut(deck, num)
            new_pos = cut2(size, new_pos, num)
        elif line.startswith("deal with increment"):
            num = int(line.split(" ")[-1])
            deck = deal_with_increment(deck, num)
            new_pos = deal_with_increment2(size, new_pos, num)
        else:
            assert line == "deal into new stack"
            deck = deal_into_new_stack(deck)
            new_pos = deal_into_new_stack2(size, new_pos)
    return new_pos


def get_input(filename: str) -> str:
    with open(filename) as f:
        data = f.read()
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='input.txt')
    args = parser.parse_args()
    data = get_input(args.filename)
    print(sol1(data))
    print(sol2(data))
    return 0


if __name__ == '__main__':
    exit(main())
