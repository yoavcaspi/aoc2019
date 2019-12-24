from __future__ import annotations
import argparse
import sys
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Set
import copy


def next_pos(x, y):
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


def sol1(data: str) -> int:
    portals_outer_names: Dict[str, Tuple[int, int]] = {}
    portals_outer: Dict[Tuple[int, int], str] = {}
    portals_inner_names: Dict[str, Tuple[int, int]] = {}
    portals_inner: Dict[Tuple[int, int], str] = {}
    board: Dict[Tuple[int, int], str] = defaultdict(lambda: ' ')
    lines = data.splitlines()
    max_x = len(lines[3])
    max_y = len(lines)
    for y, line in enumerate(lines[2:-2]):
        for x, c in enumerate(line[2:-2]):
            board[x, y] = c
            portal_name = None
            outer_flag = None
            if c == ".":
                if x == 0:
                    outer_flag = True
                    portal_name = line[:2]
                elif x == (len(line) - 5):
                    outer_flag = True
                    portal_name = line[-2:]
                elif y == 0:
                    outer_flag = True
                    portal_name = lines[0][x + 2] + lines[1][x + 2]
                elif y == (len(lines) - 5):
                    outer_flag = True
                    portal_name = lines[-2][x + 2] + lines[-1][x + 2]
                elif lines[y + 3][x + 2].isupper():
                    outer_flag = False
                    portal_name = lines[y + 3][x + 2] + lines[y + 4][x + 2]
                elif lines[y + 1][x + 2].isupper():
                    outer_flag = False
                    portal_name = lines[y][x + 2] + lines[y + 1][x + 2]
                elif line[x + 2 - 1].isupper():
                    outer_flag = False
                    portal_name = line[x + 2 - 2:x + 2]
                elif line[x + 2 + 1].isupper():
                    outer_flag = False
                    portal_name = line[x + 2 + 1:x + 2 + 3]
            if portal_name is not None:
                if outer_flag:
                    portals_outer_names[portal_name] = (x, y)
                    portals_outer[(x, y)] = portal_name
                else:
                    portals_inner_names[portal_name] = (x, y)
                    portals_inner[(x, y)] = portal_name
    my_location = portals_outer_names["AA"]
    my_path = ["AA"]
    steps = find_min_solution(board, my_location, 0, my_path, portals_outer_names, portals_outer, portals_inner_names,
                              portals_inner)
    return steps


def find_min_solution(board: Dict[Tuple[int, int], str],
                      option: Tuple[int, int],
                      steps: int,
                      my_path: List[str],
                      portals_outer_names: Dict[str, Tuple[int, int]],
                      portals_outer: Dict[Tuple[int, int], str],
                      portals_inner_names: Dict[str, Tuple[int, int]],
                      portals_inner: Dict[Tuple[int, int], str],
                      ) -> int:
    new_options = find_next_options(option, board, portals_outer_names["ZZ"])
    solutions = []
    for option, new_steps in new_options:
        if option in portals_outer:
            portal_name = portals_outer[option]
            if portal_name in my_path:
                solutions.append(sys.maxsize)
                break
            my_path.append(portal_name)
            if portal_name != "ZZ":
                new_option = portals_inner_names[portal_name]
                solutions.append(
                    find_min_solution(board, new_option, steps + new_steps + 1, my_path[:], portals_outer_names,
                                      portals_outer, portals_inner_names, portals_inner))
            else:
                solutions.append(steps + new_steps)
        else:
            assert option in portals_inner
            portal_name = portals_inner[option]
            if portal_name in my_path:
                solutions.append(sys.maxsize)
                break
            my_path.append(portal_name)
            new_option = portals_outer_names[portal_name]
            solutions.append(
                find_min_solution(board, new_option, steps + new_steps + 1, my_path[:], portals_outer_names,
                                  portals_outer,
                                  portals_inner_names, portals_inner))

    return min(solutions)


def find_next_options(my_location: Tuple[int, int],
                      board: Dict[Tuple[int, int], str],
                      final_location: Tuple[int, int],
                      ) -> List[Tuple[Tuple[int, int], int]]:
    visited: Set[Tuple[int, int]] = {my_location}
    next_steps = [(my_location, 0)]
    options = []
    while next_steps:
        position, steps = next_steps.pop()
        for pos in next_pos(*position):
            if pos == final_location:
                options.append((pos, steps + 1))
                return options
            if board[pos] == '.' and pos not in visited:
                visited.add(pos)
                next_steps.append((pos, steps + 1))
            elif (board[pos].isupper() or board[pos] == " ") and position != my_location:
                options.append((position, steps))
    return options


def sol2(data: str) -> int:
    portals_outer_names: Dict[str, Tuple[int, int]] = {}
    portals_outer: Dict[Tuple[int, int], str] = {}
    portals_inner_names: Dict[str, Tuple[int, int]] = {}
    portals_inner: Dict[Tuple[int, int], str] = {}
    board: Dict[Tuple[int, int], str] = defaultdict(lambda: ' ')
    lines = data.splitlines()
    max_x = len(lines[3])
    max_y = len(lines)
    for y, line in enumerate(lines[2:-2]):
        for x, c in enumerate(line[2:-2]):
            board[x, y] = c
            portal_name = None
            outer_flag = None
            if c == ".":
                if x == 0:
                    outer_flag = True
                    portal_name = line[:2]
                elif x == (len(line) - 5):
                    outer_flag = True
                    portal_name = line[-2:]
                elif y == 0:
                    outer_flag = True
                    portal_name = lines[0][x + 2] + lines[1][x + 2]
                elif y == (len(lines) - 5):
                    outer_flag = True
                    portal_name = lines[-2][x + 2] + lines[-1][x + 2]
                elif lines[y + 3][x + 2].isupper():
                    outer_flag = False
                    portal_name = lines[y + 3][x + 2] + lines[y + 4][x + 2]
                elif lines[y + 1][x + 2].isupper():
                    outer_flag = False
                    portal_name = lines[y][x + 2] + lines[y + 1][x + 2]
                elif line[x + 2 - 1].isupper():
                    outer_flag = False
                    portal_name = line[x + 2 - 2:x + 2]
                elif line[x + 2 + 1].isupper():
                    outer_flag = False
                    portal_name = line[x + 2 + 1:x + 2 + 3]
            if portal_name is not None:
                if outer_flag:
                    portals_outer_names[portal_name] = (x, y)
                    portals_outer[(x, y)] = portal_name
                else:
                    portals_inner_names[portal_name] = (x, y)
                    portals_inner[(x, y)] = portal_name
    my_location = portals_outer_names["AA"]
    my_path = [("AA", 0, True)]
    steps = find_min_solution2(board, my_location, 0, 0, my_path, portals_outer_names, portals_outer, portals_inner_names,
                               portals_inner)
    return steps


def find_min_solution2(board: Dict[Tuple[int, int], str],
                       cur_option: Tuple[int, int],
                       my_level: int,
                       steps: int,
                       my_path: List[Tuple[str, int, bool]],
                       portals_outer_names: Dict[str, Tuple[int, int]],
                       portals_outer: Dict[Tuple[int, int], str],
                       portals_inner_names: Dict[str, Tuple[int, int]],
                       portals_inner: Dict[Tuple[int, int], str],
                       ) -> int:
    new_options = find_next_options2(cur_option, board, portals_outer_names["ZZ"])
    solutions = []
    if my_level > 30:
        return sys.maxsize
    for option, new_steps in new_options:
        if option in portals_outer:
            portal_name = portals_outer[option]
            if (portal_name, my_level, True) in my_path:
                solutions.append(sys.maxsize)
                break
            if portal_name not in ("ZZ", "AA") and my_level > 0:
                my_path.append((portal_name, my_level, True))
                new_option = portals_inner_names[portal_name]
                solutions.append(
                    find_min_solution2(board, new_option, my_level - 1, steps + new_steps + 1, my_path[:], portals_outer_names,
                                      portals_outer, portals_inner_names, portals_inner))
                my_path.pop()
            elif portal_name == "ZZ" and my_level == 0:
                solutions.append(steps + new_steps)
        else:
            assert option in portals_inner
            portal_name = portals_inner[option]
            if (portal_name, my_level, False) in my_path:
                solutions.append(sys.maxsize)
                break
            my_path.append((portal_name, my_level, False))
            new_option = portals_outer_names[portal_name]
            solutions.append(
                find_min_solution2(board, new_option, my_level + 1, steps + new_steps + 1, my_path[:], portals_outer_names,
                                  portals_outer,
                                  portals_inner_names, portals_inner))
            my_path.pop()
    return min(solutions + [sys.maxsize])


def find_next_options2(my_location: Tuple[int, int],
                      board: Dict[Tuple[int, int], str],
                      final_location: Tuple[int, int],
                      ) -> List[Tuple[Tuple[int, int], int]]:
    visited: Set[Tuple[int, int]] = {my_location}
    next_steps = [(my_location, 0)]
    options = []
    while next_steps:
        position, steps = next_steps.pop()
        for pos in next_pos(*position):
            if pos == final_location:
                options.append((pos, steps + 1))
            if board[pos] == '.' and pos not in visited:
                visited.add(pos)
                next_steps.append((pos, steps + 1))
            elif (board[pos].isupper() or board[pos] == " ") and position != my_location:
                options.append((position, steps))
    return options



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
