from __future__ import annotations
import argparse
from collections import defaultdict
from typing import List, Dict, Optional, Tuple, Set
from os import system


class Opcode:
    def __init__(self):
        self.instruction_size = 0

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int, int],
            *vals) -> Optional[int]:
        raise NotImplemented()

    def get_parameter(self, data: List[int], mode: int, val: int, rel_base: int, extended_mem: Dict[int, int]) -> int:
        if mode == 0:
            if val > len(data):
                return extended_mem[val]
            else:
                return data[val]
        elif mode == 1:
            return val
        elif mode == 2:
            if rel_base + val >= len(data):
                return extended_mem[rel_base + val]
            else:
                return data[rel_base + val]
        else:
            breakpoint()


class Operand(Opcode):
    pass


class Add(Operand):
    def __init__(self):
        super().__init__()
        self.instruction_size = 4

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int, int],
            *vals) -> Optional[int]:
        assert len(vals) == 3
        retval = 0
        for i in range(self.instruction_size - 2):
            modes, mode = divmod(modes, 10)
            retval += self.get_parameter(data, mode, vals[i], rel_path, extended_mem)

        modes, mode = divmod(modes, 10)
        if mode == 2:
            address = rel_path + vals[2]
        else:
            address = vals[2]
        if address >= len(data):
            extended_mem[address] = retval
        else:
            data[address] = retval
        return None


class Mul(Operand):
    def __init__(self):
        super().__init__()
        self.instruction_size = 4

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int, int],
            *vals) -> Optional[int]:
        assert len(vals) == 3
        retval = 1
        for i in range(self.instruction_size - 2):
            modes, mode = divmod(modes, 10)
            retval *= self.get_parameter(data, mode, vals[i], rel_path, extended_mem)
        modes, mode = divmod(modes, 10)
        if mode == 2:
            address = rel_path + vals[2]
        else:
            address = vals[2]
        if address >= len(data):
            extended_mem[address] = retval
        else:
            data[address] = retval
        return None


class Io(Opcode):
    pass


class Input(Io):
    def __init__(self):
        super().__init__()
        self.instruction_size = 2

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int, int],
            *vals) -> Optional[int]:
        assert len(vals) == 1
        modes, mode = divmod(modes, 10)
        assert mode in (0, 2)
        if mode == 0:
            address = vals[0]
        elif mode == 2:
            address = rel_path + vals[0]
        else:
            breakpoint()
        # address = self.get_parameter(data, mode, vals[0], rel_path, extended_mem)
        if address >= len(data):
            extended_mem[address] = input_data.pop(0)
        else:
            data[address] = input_data.pop(0)
        return None


class Output(Io):
    def __init__(self):
        super().__init__()
        self.instruction_size = 2

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int, int],
            *vals) -> Optional[int]:
        assert len(vals) == 1
        return self.get_parameter(data, modes, vals[0], rel_path, extended_mem)


class ConditionalJump(Opcode):
    def __init__(self):
        super().__init__()
        self.instruction_size = 3
        self.jump_to = -1

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int, int],
            *vals) -> Optional[int]:
        val: int = 0
        modes, mode = divmod(modes, 10)
        val = self.get_parameter(data, mode, vals[0], rel_path, extended_mem)
        modes, mode = divmod(modes, 10)
        self.jump_to = self.get_parameter(data, mode, vals[1], rel_path, extended_mem)
        return self.condition(val)

    def condition(self, val: int) -> Optional[int]:
        raise NotImplemented()

    def get_new_ip(self):
        return self.jump_to


class JumpIfTrue(ConditionalJump):
    def condition(self, val: int) -> bool:
        return bool(val)


class JumpIfFalse(ConditionalJump):
    def condition(self, val: int) -> bool:
        return not val


class ConditionalStore(Opcode):
    def __init__(self):
        super().__init__()
        self.instruction_size = 4

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int, int],
            *vals) -> Optional[int]:
        modes, mode = divmod(modes, 10)
        val1 = self.get_parameter(data, mode, vals[0], rel_path, extended_mem)
        modes, mode = divmod(modes, 10)
        val2 = self.get_parameter(data, mode, vals[1], rel_path, extended_mem)
        modes, mode = divmod(modes, 10)
        if mode == 2:
            address = rel_path + vals[2]
        else:
            address = vals[2]

        if self.condition(val1, val2):
            if address > len(data):
                extended_mem[address] = 1
            else:
                data[address] = 1
        else:
            if address > len(data):
                extended_mem[address] = 0
            else:
                data[address] = 0

    def condition(self, val1: int, val2: int) -> bool:
        raise NotImplemented()


class LessThan(ConditionalStore):
    def condition(self, val1: int, val2: int) -> bool:
        return val1 < val2


class Equals(ConditionalStore):
    def condition(self, val1: int, val2: int) -> bool:
        return val1 == val2


class AdjustRelPath(Opcode):
    def __init__(self):
        super().__init__()
        self.instruction_size = 2

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int, int],
            *vals) -> Optional[int]:
        modes, mode = divmod(modes, 10)
        val = self.get_parameter(data, mode, vals[0], rel_path, extended_mem)
        return rel_path + val


opcodes: Dict[int, Opcode] = dict(
    ((1, Add()),
     (2, Mul()),
     (3, Input()),
     (4, Output()),
     (5, JumpIfTrue()),
     (6, JumpIfFalse()),
     (7, LessThan()),
     (8, Equals()),
     (9, AdjustRelPath()),
     (99, None)))


def get_new_location(direction: int, location: Tuple[int, int]) -> Tuple[int, int]:
    if direction == 1:
        return location[0], location[1] - 1
    elif direction == 2:
        return location[0], location[1] + 1
    elif direction == 3:
        return location[0] - 1, location[1]
    elif direction == 4:
        return location[0] + 1, location[1]


def print_board(board: Dict[Tuple[int, int], str]):
    min_x = min(x for x, y in board.keys())
    min_y = min(y for x, y in board.keys())
    max_x = max(x for x, y in board.keys())
    max_y = max(y for x, y in board.keys())
    for y in range(max_y + 2, min_y - 2, -1):
        for x in range(min_x - 2, max_x + 2):
            print(board[(x, y)], end='')
        print()
    pass


DIRECTIONS = (1, 3, 2, 4)


def get_next_direction(old_direction: int) -> List[int]:
    if old_direction == 1:
        return [3, 4, 1, 2]
    elif old_direction == 2:
        return [4, 3, 2, 1]
    elif old_direction == 3:
        return [2, 1, 3, 4]
    elif old_direction == 4:
        return [1, 2, 4, 3]


def is_opposite_direction(prev_direction, cur_direction):
    return (
            (prev_direction == 1 and cur_direction == 2) or
            (prev_direction == 2 and cur_direction == 1) or
            (prev_direction == 3 and cur_direction == 4) or
            (prev_direction == 4 and cur_direction == 3)
    )


def sol1(data: str) -> int:
    line = [int(num) for num in data.split(',')]
    ir = 0
    rel_path = 0
    extended_mem = defaultdict(int)
    size = len(line)
    board: Dict[Tuple[int, int], str] = defaultdict(lambda: " ")
    current_pos = (0, 0)
    board[current_pos] = "D"

    last_direction = None

    input_data = get_next_direction(1)
    my_route = []
    my_options = []
    while ir < size:
        command = line[ir]
        modes, opcode = divmod(command, 100)
        method = opcodes[opcode]
        if method is not None:
            if isinstance(method, Input):
                last_direction = input_data[0]
                next_pos = get_new_location(last_direction, current_pos)
                print(f"my_direction is {last_direction} my location is {current_pos=} {len(board)=}")
            retval = method.run(input_data, line, modes, rel_path, extended_mem,
                                *line[ir + 1:ir + method.instruction_size])
        else:
            break
        if isinstance(method, ConditionalJump) and retval:
            ir = method.get_new_ip()
        else:
            ir += method.instruction_size
        if isinstance(method, AdjustRelPath):
            rel_path = retval
        elif not isinstance(method, ConditionalJump) and retval is not None:
            if retval == 0:
                board[next_pos] = "#"
            elif retval == 1:
                board[next_pos] = "D"
                board[current_pos] = "."
                if len(my_route) > 0:
                    if is_opposite_direction(my_route[-1], last_direction):
                        my_route.pop()
                        input_data = my_options.pop()
                    else:
                        my_route.append(last_direction)
                        my_options.append(input_data[:])
                        current_pos = next_pos
                        input_data = get_next_direction(last_direction)
                else:
                    my_route.append(last_direction)
                    my_options.append(input_data[:])
                    current_pos = next_pos
                    input_data = get_next_direction(last_direction)
            elif retval == 2:
                print_board(board)
                return len(my_route) + 1


def fill_oxygen(board: Dict[Tuple[int, int], str], pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
    new_poses = set()
    new_pos = (pos[0] - 1, pos[1])
    if board[new_pos] == ".":
        new_poses.add(new_pos)
        board[new_pos] = "X"
    new_pos = (pos[0] + 1, pos[1])
    if board[new_pos] == ".":
        new_poses.add(new_pos)
        board[new_pos] = "X"

    new_pos = (pos[0], pos[1] - 1)
    if board[new_pos] == ".":
        new_poses.add(new_pos)
        board[new_pos] = "X"

    new_pos = (pos[0], pos[1] + 1)
    if board[new_pos] == ".":
        new_poses.add(new_pos)
        board[new_pos] = "X"

    return new_poses


def sol2(data: str) -> int:
    line = [int(num) for num in data.split(',')]
    ir = 0
    rel_path = 0
    extended_mem = defaultdict(int)
    size = len(line)
    board: Dict[Tuple[int, int], str] = defaultdict(lambda: " ")
    current_pos = (0, 0)
    board[current_pos] = "D"

    last_direction = None

    input_data = get_next_direction(1)
    my_route = []
    my_options = []
    oxygen_pos = None
    while ir < size:
        command = line[ir]
        modes, opcode = divmod(command, 100)
        method = opcodes[opcode]
        if method is not None:
            if isinstance(method, Input):
                last_direction = input_data[0]
                next_pos = get_new_location(last_direction, current_pos)
            retval = method.run(input_data, line, modes, rel_path, extended_mem,
                                *line[ir + 1:ir + method.instruction_size])
        else:
            break
        if isinstance(method, ConditionalJump) and retval:
            ir = method.get_new_ip()
        else:
            ir += method.instruction_size
        if isinstance(method, AdjustRelPath):
            rel_path = retval
        elif not isinstance(method, ConditionalJump) and retval is not None:
            # print(f"{len(my_route)=} {len(input_data)=} {current_pos=} {len(board)=}")

            if retval == 0:
                board[next_pos] = "#"
            elif retval in (1, 2):
                if retval == 2:
                    oxygen_pos = next_pos
                    board[oxygen_pos] = "X"
                else:
                    board[next_pos] = "D"
                if oxygen_pos is None or current_pos != oxygen_pos:
                    board[current_pos] = "."
                if len(my_route) > 0:
                    if is_opposite_direction(my_route[-1], last_direction):
                        my_route.pop()
                        current_pos = next_pos
                        input_data = my_options.pop()
                    else:
                        my_route.append(last_direction)
                        my_options.append(input_data[:])
                        current_pos = next_pos
                        input_data = get_next_direction(last_direction)
                else:
                    my_route.append(last_direction)
                    my_options.append(input_data[:])
                    current_pos = next_pos
                    input_data = get_next_direction(last_direction)
            if len(my_route) == 0 and len(input_data) == 0:
                # print_board(board)
                board[0, 0] = '.'
                break
    counter = 0
    oxygen_positons = {oxygen_pos}
    while len(oxygen_positons) != 0:
        counter += 1
        new_oxygen_positions = set()
        for pos in oxygen_positons:
            new_oxygen_positions = new_oxygen_positions.union(fill_oxygen(board, pos))
        oxygen_positons = new_oxygen_positions
    return counter - 1


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
