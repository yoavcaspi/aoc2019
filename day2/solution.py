import argparse
from typing import List, Dict, Any


def add(x, y):
    return x+y


def mul(x, y):
    return x*y


opcodes: Dict[int, Any] = dict(((1, add), (2, mul), (99, None)))


def sol1(data: List[int]) -> int:
    i = 0
    size = len(data)
    while i < size:
        opcode = data[i]
        method = opcodes[opcode]
        if method is not None:
            data[data[i + 3]] = method(data[data[i + 1]], data[data[i + 2]])
        else:
            break
        i += 4
    return data[0]


def sol2(data: List[str]) -> int:
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
    new_data = [int(x) for x in data[0].split(',')]
    new_data[1] = 12
    new_data[2] = 2
    print(sol1(new_data))
    print(sol2(data))
    return 0


if __name__ == '__main__':
    exit(main())
