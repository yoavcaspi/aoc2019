from __future__ import annotations
import argparse
from typing import List, Dict, Tuple, Optional, Set
import copy


def next_pos(x, y):
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


def sol1(data: str) -> int:
    board: Dict[Tuple[int, int], str] = {}
    my_location: Optional[Tuple[int, int]] = None
    keys_count: int = 0
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == "@":
                my_location = (x, y)
            if c.islower():
                keys_count += 1
            board[(x, y)] = c
    visited = set()
    states = [(frozenset(), my_location, 0)]
    while True:
        next_states = []
        for keys, (x, y), steps in states:
            for next_x, next_y in next_pos(x, y):
                c = board[(next_x, next_y)]
                if (keys, (next_x, next_y)) in visited:
                    continue
                elif c == "#":
                    continue
                elif c.isupper() and c.lower() not in keys:
                    continue

                if c.islower() and c not in keys:
                    cand_keys = keys | {c}
                else:
                    cand_keys = keys

                visited.add((keys, (next_x, next_y)))
                next_states.append((cand_keys, (next_x, next_y), steps + 1))

                if len(keys) == keys_count:
                    return steps
        states = next_states


def fix_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ",":
                board[i][j] = "."


def find_min_sol(board: List[List[str]],
                 doors_locations: Dict[str, Tuple[int, int]],
                 my_location: Tuple[int, int], path: List[str], left_keys: Set[str]) -> int:
    keys_shortest_path: Dict[str, Tuple[Tuple[int, int], int]] = find_available_keys(copy.deepcopy(board), my_location)

    if len(keys_shortest_path) == 0:
        print(path)
        return 0
    else:
        solutions = []
        for key, val in keys_shortest_path.items():
            (x, y), score = val
            board[y][x] = "@"
            door_x, door_y = doors_locations.get(key.upper(), (0, 0))
            board[door_y][door_x] = "."
            board[my_location[1]][my_location[0]] = "."
            path.append(key)
            print(path)
            left_keys.remove(key)
            if min_paths.get((key, frozenset(left_keys)), None) is not None:
                return score + min_paths[(key, frozenset(left_keys))]
            new_score = find_min_sol(copy.deepcopy(board),
                                     doors_locations,
                                     (x, y),
                                     path[:],
                                     copy.deepcopy(left_keys))
            min_paths[(key, frozenset(left_keys))] = new_score
            solutions.append(score + new_score)
            path.pop()
            left_keys.add(key)
            board[door_y][door_x] = key.upper()
            board[y][x] = key
            board[my_location[1]][my_location[0]] = "@"

        return min(solutions)


def sol2(data: str) -> int:
    return 2


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
