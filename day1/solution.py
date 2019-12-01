import argparse
from typing import List


def sol1(data: List[str]) -> int:
    res = 0
    for line in data:
        res += int(line) // 3 - 2
    return res


def calculate_fuel(module_mass: int) -> int:
    new_mass = module_mass
    res = 0
    while new_mass > 0:
        new_mass = max(new_mass // 3 - 2, 0)
        res += new_mass
    return res


def sol2(data: List[str]) -> int:
    res = 0
    stop_flag = False
    for line in data:
        res += calculate_fuel(int(line))
    return res


def get_input(filename: str) -> List[str]:
    with open(filename) as f:
        lines = f.readlines()
    return lines


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
