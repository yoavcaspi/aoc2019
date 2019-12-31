from __future__ import annotations
import argparse
from typing import Tuple, Dict, Set
from collections import defaultdict


def neighbors_pos(x: int, y: int) -> Tuple[int, int]:
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


def sol1(data: str) -> int:
    seen_boards: Set[Tuple[Tuple[int, int], ...]] = set()
    board: Dict[Tuple[int, int], str] = defaultdict(str)
    neighbors_count: Dict[Tuple[int, int], int] = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            board[(x, y)] = c
    while tuple(board.items()) not in seen_boards:
        seen_boards.add(tuple(board.items()))
        for y in range(5):
            for x in range(5):
                neighbors_count[(x, y)] = sum((1 for n_x, n_y in neighbors_pos(x, y) if board[(n_x, n_y)] == "#"))

        for y in range(5):
            for x in range(5):
                if board[x, y] == "#" and neighbors_count[x, y] != 1:
                    board[x, y] = "."
                elif board[x, y] == "." and neighbors_count[x, y] in (1, 2):
                    board[x, y] = "#"
    ret_val: int = 0
    for y in range(5):
        for x in range(5):
            if board[x, y] == "#":
                ret_val += 2 ** (y * 5 + x)
    return ret_val


def sol2(data: str, num_minutes=200) -> int:
    board: Dict[Tuple[int, int, int], str] = defaultdict(lambda: ".")
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            board[(x, y, 0)] = c
    for i in range(num_minutes):
        neighbors_count: Dict[Tuple[int, int, int], int] = defaultdict(int)
        for j in range((-num_minutes - 1) // 2, (num_minutes + 2) // 2):
            # regular neighbors
            for y in range(5):
                for x in range(5):
                    if x == 2 and y == 2:
                        continue
                    neighbors_count[(x, y, j)] += sum(
                        (1 for n_x, n_y in neighbors_pos(x, y) if board[(n_x, n_y, j)] == "#"))

            # inner neighbors
            if board[(2, 1, j)] == "#":
                for x in range(5):
                    neighbors_count[(x, 0, j + 1)] += 1
            if board[(2, 3, j)] == "#":
                for x in range(5):
                    neighbors_count[(x, 4, j + 1)] += 1
            if board[(1, 2, j)] == "#":
                for y in range(5):
                    neighbors_count[(0, y, j + 1)] += 1
            if board[(3, 2, j)] == "#":
                for y in range(5):
                    neighbors_count[(4, y, j + 1)] += 1

            # outer neighbors
            for x in range(5):
                if board[(x, 0, j)] == "#":
                    neighbors_count[(2, 1, j - 1)] += 1
                if board[(x, 4, j)] == "#":
                    neighbors_count[(2, 3, j - 1)] += 1
            # outer neighbors
            for y in range(5):
                if board[(0, y, j)] == "#":
                    neighbors_count[(1, 2, j - 1)] += 1
                if board[(4, y, j)] == "#":
                    neighbors_count[(3, 2, j - 1)] += 1

        for j in range((-num_minutes - 1) // 2, (num_minutes + 2) // 2):
            for y in range(5):
                for x in range(5):
                    if x == 2 and y == 2:
                        board[x, y, j] = "."
                        continue
                    if board[x, y, j] == "#" and neighbors_count[x, y, j] != 1:
                        board[x, y, j] = "."
                    elif board[x, y, j] == "." and neighbors_count[x, y, j] in (1, 2):
                        board[x, y, j] = "#"

    count = 0
    for i in range((-num_minutes - 1) // 2, (num_minutes + 2) // 2):
        for y in range(5):
            for x in range(5):
                if board[(x, y, i)] == "#":
                    count += 1
    return count


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
