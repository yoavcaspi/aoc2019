from __future__ import annotations
import argparse
import itertools
from typing import Optional


def sol1(data: str, phases: Optional[int] = 100) -> str:
    new_data1 = [int(a) for a in data if a != "\n"]
    new_data2 = []
    for i in range(phases):
        for j in range(1, len(data) + 1):
            pattern = [0] * j + [1] * j + [0] * j + [-1] * j
            cycle = itertools.cycle(pattern)
            # Skip the first value
            next(cycle)
            val = sum(digit * digit_p for digit, digit_p in zip(new_data1, cycle))
            val_digit = abs(val) % 10
            new_data2.append(val_digit)
        new_data1 = new_data2[:]
        new_data2.clear()
    return "".join([str(val) for val in new_data1[:8]])


def sol2(data: str, phases: Optional[int] = 100) -> str:
    orig_data = [int(a) for a in data.strip()] * 10_000
    digits_to_skip = int(data[:7])
    assert len(orig_data) // 2 < digits_to_skip
    new_data = orig_data[digits_to_skip:]
    for i in range(phases):
        last_digit = new_data[-1]
        new_data2 = [last_digit]
        for val in reversed(new_data[:-1]):
            last_digit = (last_digit + val) % 10
            new_data2.append(last_digit)
        new_data = new_data2[::-1]
    return "".join([str(val) for val in new_data[:8]])


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
