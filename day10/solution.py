import argparse
import math
from typing import List, Tuple


def sol1(data: str) -> int:
    grid = []
    for row in data.split('\n'):
        if row == '':
            break
        grid.append([])
        for column in row:
            grid[-1].append(column)
    width = len(grid[0])
    height = len(grid)
    results = []
    for x in range(width):
        for y in range(height):
            if grid[y][x] != "#":
                continue
            playgroud = [['.' for _ in range(width)] for _ in range(height)]
            playgroud[y][x] = "X"
            res = 0
            for i in range(0, width - x):
                for j in range(0, height - y):
                    k = x + i
                    l = y + j
                    flag = False
                    while 0 <= k < width and 0 <= l < height and playgroud[l][k] != "X":
                        if grid[l][k] == "#" and not flag:
                            flag = True
                        playgroud[l][k] = "X"
                        k += i
                        l += j
                    if flag:
                        res += 1

            for i in reversed(range(-x, 0)):
                for j in range(0, height - y):
                    k = x + i
                    l = y + j
                    flag = False
                    while 0 <= k < width and 0 <= l < height and playgroud[l][k] != "X":
                        if grid[l][k] == "#" and not flag:
                            flag = True
                        playgroud[l][k] = "X"
                        k += i
                        l += j
                    if flag:
                        res += 1
            for i in range(0, width - x):
                for j in reversed(range(-y, 0)):
                    k = x + i
                    l = y + j
                    flag = False
                    while 0 <= k < width and 0 <= l < height and playgroud[l][k] != "X":
                        if grid[l][k] == "#" and not flag:
                            flag = True
                        playgroud[l][k] = "X"
                        k += i
                        l += j
                    if flag:
                        res += 1
            for i in reversed(range(-x, 0)):
                for j in reversed(range(-y, 0)):
                    k = x + i
                    l = y + j
                    flag = False
                    while 0 <= k < width and 0 <= l < height and playgroud[l][k] != "X":
                        if grid[l][k] == "#" and not flag:
                            flag = True
                        playgroud[l][k] = "X"
                        k += i
                        l += j
                    if flag:
                        res += 1
            results.append((res, x, y))
    max_val = max(results, key=lambda x: x[0])
    print(f"{max_val[1]=} {max_val[2]=}")
    return max_val[0]


def sol2(data: str) -> int:
    grid = []
    for row in data.split('\n'):
        if row == '':
            break
        grid.append([])
        for column in row:
            grid[-1].append(column)
    width = len(grid[0])
    height = len(grid)
    x = 20
    y = 19
    assert grid[y][x] == "#"
    playgroud: List[List[str]] = [['.' for _ in range(width)] for _ in range(height)]
    playgroud[y][x] = "X"
    asteroids_angles: List[Tuple[int, int, int]] = []

    for i in range(0, width - x):
        for j in reversed(range(-y, 0)):
            k = x + i
            l = y + j
            flag = False
            while 0 <= k < width and 0 <= l < height and playgroud[l][k] != "X":
                if grid[l][k] == "#" and not flag:
                    flag = True
                    asteroids_angles.append((x + i, y + j, math.atan2(j, i)))
                playgroud[l][k] = "X"
                k += i
                l += j

    for i in range(0, width - x):
        for j in range(0, height - y):
            k = x + i
            l = y + j
            flag = False
            while 0 <= k < width and 0 <= l < height and playgroud[l][k] != "X":
                if grid[l][k] == "#" and not flag:
                    flag = True
                    asteroids_angles.append((x + i, y + j, math.atan2(j, i)))
                playgroud[l][k] = "X"
                k += i
                l += j

    for j in range(0, height - y):
        for i in reversed(range(-x, 0)):
            k = x + i
            l = y + j
            flag = False
            while 0 <= k < width and 0 <= l < height and playgroud[l][k] != "X":
                if grid[l][k] == "#" and not flag:
                    flag = True
                    asteroids_angles.append((x + i, y + j, math.atan2(j, i)))
                playgroud[l][k] = "X"
                k += i
                l += j

    for i in reversed(range(-x, 0)):
        for j in reversed(range(-y, 0)):
            k = x + i
            l = y + j
            flag = False
            while 0 <= k < width and 0 <= l < height and playgroud[l][k] != "X":
                if grid[l][k] == "#" and not flag:
                    flag = True
                    asteroids_angles.append((x + i, y + j, math.atan2(j, i) + 2 * math.pi))
                playgroud[l][k] = "X"
                k += i
                l += j

    asteroids_angles.sort(key=lambda x: x[2])
    return asteroids_angles[199][0] * 100 + asteroids_angles[199][1]


def get_input(filename: str) -> str:
    with open(filename) as f:
        lines = f.read()
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
