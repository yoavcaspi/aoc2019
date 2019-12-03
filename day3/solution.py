import argparse
import sys
from collections import defaultdict
from typing import List, Tuple, Dict


class CentralPort:
    def __init__(self):
        self.current_pos: Tuple[int, int] = (0, 0)
        self.board: Dict[Tuple[int, int], str] = defaultdict(lambda: '.')
        self.board[(0, 0)] = 'o'
        self.board_step = {(0, 0): 0}
        self.wire_step = {'0': 0, '1': 0}
        self.closest_point_dist: int = sys.maxsize
        self.closest_steps_dist: int = sys.maxsize

    def move(self, direction: str, wire_type: str):
        x, y = self.current_pos
        if direction == 'R':
            x += 1
        elif direction == 'U':
            y += 1
        elif direction == 'L':
            x -= 1
        elif direction == 'D':
            y -= 1
        self.wire_step[wire_type] += 1
        self.current_pos = (x, y)

    def add_wire(self, direction: str, count: int, wire_type: str):
        if direction not in 'RULD':
            raise ValueError(f"{direction=} not one of RULD")
        for i in range(count):
            self.move(direction, wire_type)
            if self.board[self.current_pos] == '.':
                self.board[self.current_pos] = wire_type
                self.board_step[self.current_pos] = self.wire_step[wire_type]
            elif self.board[self.current_pos] != wire_type:
                self.add_crossing_point(self.current_pos)

    def add_crossing_point(self, pos):
        self.closest_point_dist = min(self.closest_point_dist, abs(pos[0]) + abs(pos[1]))
        self.closest_steps_dist = min(self.closest_steps_dist, self.board_step[self.current_pos] + self.wire_step['1'])

    def print_board(self):
        min_x = min(x for x, y in self.board.keys())
        min_y = min(y for x, y in self.board.keys())
        max_x = max(x for x, y in self.board.keys())
        max_y = max(y for x, y in self.board.keys())
        for y in range(max_y + 10, min_y - 10, -1):
            for x in range(min_x - 10, max_x + 10):
                print(self.board[(x,y)],end='')
            print()


def sol1(data: List[str]) -> int:
    central_port = CentralPort()
    for i, directions in enumerate(data):
        for direction_string in directions.split(','):
            central_port.add_wire(direction_string[0], int(direction_string[1:]), str(i))
        central_port.current_pos = (0, 0)
    return central_port.closest_point_dist


def sol2(data: List[str]) -> int:
    central_port = CentralPort()
    for i, directions in enumerate(data):
        for direction_string in directions.split(','):
            central_port.add_wire(direction_string[0], int(direction_string[1:]), str(i))
        central_port.current_pos = (0, 0)
    return central_port.closest_steps_dist


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
