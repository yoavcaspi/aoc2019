import argparse
from typing import List


def sol1(data: List[str]) -> int:
    res = 0
    for line in data:
        res += int(line) // 3 -2
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
    return 0


if __name__ == '__main__':
    exit(main())
