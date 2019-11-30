import argparse
from typing import List


def sol() -> int:
    return 1


def get_input(filename: str) -> List[str]:
    with open(filename) as f:
        lines = f.readlines()
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='input.txt')
    args = parser.parse_args()
    data = get_input(args.filename)
    sol()
    return 0


if __name__ == '__main__':
    exit(main())
