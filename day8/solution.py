import argparse
from typing import List
from collections import Counter


def sol1(data: str) -> int:
    wide = 25
    tall = 6
    layers = []
    layers_data = []
    prev = 0
    for i in range(wide*tall, len(data), wide*tall):
        layers.append(data[prev:i])
        prev = i
        layers_data.append(Counter(layers[-1]))
    min_layer = min(layers_data, key = lambda x: x['0'])
    return min_layer['1'] * min_layer['2']


def sol2(data: str) -> int:
    wide = 25
    tall = 6
    layers = []
    picture = ''
    prev = 0
    for i in range(wide*tall, len(data), wide*tall):
        layers.append(data[prev:i])
        prev = i

    for i in range(wide * tall):
        for j, layer in enumerate(layers):
            if layer[i] != '2':
                print(j)
                if layer[i] == '1':
                    picture += '#'
                else:
                    picture += ' '
                break
    prev = 0
    for i in range(wide, wide*tall +1, wide):
        print(picture[prev:i])
        prev = i
    return 0

def get_input(filename: str) -> List[str]:
    with open(filename) as f:
        lines = f.readlines()
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='input.txt')
    args = parser.parse_args()
    data = get_input(args.filename)
    print(sol1(data[0]))
    print(sol2(data[0]))
    return 0


if __name__ == '__main__':
    exit(main())
