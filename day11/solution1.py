import argparse
from typing import List, Dict, Optional, Tuple
from collections import Counter, defaultdict

import pytest


class Opcode:
    def __init__(self):
        self.instruction_size = 0

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int,int], *vals) -> Optional[int]:
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
            if rel_base + val > len(data):
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

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int,int], *vals) -> Optional[int]:
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
        if address > len(data):
            extended_mem[address] = retval
        else:
            data[address] = retval
        return None


class Mul(Operand):
    def __init__(self):
        super().__init__()
        self.instruction_size = 4

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int,int], *vals) -> Optional[int]:
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
        if address > len(data):
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

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int,int], *vals) -> Optional[int]:
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
        if address > len(data):
            extended_mem[address] = input_data.pop(0)
        else:
            data[address] = input_data.pop(0)
        return None


class Output(Io):
    def __init__(self):
        super().__init__()
        self.instruction_size = 2

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int,int], *vals) -> Optional[int]:
        assert len(vals) == 1
        return self.get_parameter(data, modes, vals[0], rel_path, extended_mem)


class ConditionalJump(Opcode):
    def __init__(self):
        super().__init__()
        self.instruction_size = 3
        self.jump_to = -1

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int,int], *vals) -> Optional[int]:
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

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int,int], *vals) -> Optional[int]:
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

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int,int], *vals) -> Optional[int]:
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


def change_direction(current_pos, direction, turn_right_or_left):
    # 0 - up, 1 - right, 2 - down, 3 - left
    if turn_right_or_left == 1:
        new_direction = (direction + 1) % 4
    else:
        new_direction = (direction - 1) % 4
    if new_direction == 0:
        new_pos = current_pos[0] - 1, current_pos[1]
    elif new_direction == 1:
        new_pos = current_pos[0], current_pos[1] + 1

    elif new_direction == 2:
        new_pos = current_pos[0] + 1, current_pos[1]
    else:
        assert new_direction == 3
        new_pos = current_pos[0], current_pos[1] - 1
    return new_pos, new_direction


def sol(data: str) -> int:
    line = [int(num) for num in data.split(',')]
    ir = 0
    rel_path = 0
    extended_mem = defaultdict(int)
    grid: Dict[Tuple[int, int], int] = defaultdict(lambda: 0)
    current_pos = (0, 0)
    direction = 0
    grid[current_pos], rel_path, ir, extended_mem, was_stopped = compute(line, [grid[current_pos]], rel_path, extended_mem, ir)
    turn_right_or_left, rel_path, ir, extended_mem, was_stopped = compute(line, [], rel_path, extended_mem, ir)
    current_pos, direction = change_direction(current_pos, direction, turn_right_or_left)
    while not was_stopped:
        grid[current_pos], rel_path, ir, extended_mem, was_stopped = compute(line, [grid[current_pos]], rel_path,
                                                                             extended_mem, ir)
        turn_right_or_left, rel_path, ir, extended_mem, was_stopped = compute(line, [], rel_path,
                                                                         extended_mem, ir)
        current_pos, direction = change_direction(current_pos, direction, turn_right_or_left)
    return len(grid.keys()) -1


def compute(data, input_data, rel_path, extended_mem, ir):
    retval2 = None
    size = len(data)
    was_stopped = False
    while ir < size:
        command = data[ir]
        modes, opcode = divmod(command, 100)
        method = opcodes[opcode]
        if method is not None:
            retval = method.run(input_data, data, modes, rel_path, extended_mem, *data[ir + 1:ir + method.instruction_size])
        else:
            was_stopped = True
            break
        if isinstance(method, ConditionalJump) and retval:
            ir = method.get_new_ip()
        else:
            ir += method.instruction_size
        if isinstance(method, AdjustRelPath):
            rel_path = retval
        elif not isinstance(method, ConditionalJump) and retval is not None:
            print(retval)
            retval2 = retval
            break
    # print(f"{ir=}")
    return retval2, rel_path, ir, extended_mem, was_stopped


def get_input(filename: str) -> str:
    with open(filename) as f:
        data = f.read()
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='input.txt')
    args = parser.parse_args()
    data = get_input(args.filename)
    print(sol(data))
    return 0


if __name__ == '__main__':
    exit(main())
