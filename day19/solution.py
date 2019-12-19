from __future__ import annotations
import argparse
from collections import defaultdict
from typing import List, Dict, Optional


class Opcode:
    def __init__(self):
        self.instruction_size = 0

    def run(self, input_data: List[int], data: List[int], modes: int, rel_path: int, extended_mem: Dict[int, int],
            *vals) -> Optional[int]:
        raise NotImplemented()

    def get_parameter(self, data: List[int], mode: int, val: int, rel_base: int, extended_mem: Dict[int, int]) -> int:
        if mode == 0:
            if val >= len(data):
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


def sol1(data: str) -> int:
    line = [int(num) for num in data.split(',')]
    ir = 0
    rel_path = 0
    extended_mem = defaultdict(int)
    size = len(line)
    board: List[List[str]] = [[" " for _ in range(50)] for _ in range(50)]
    for i in range(50):
        for j in range(50):
            input_data = [i, j]
            board[i][j] = run_IntCode(extended_mem, input_data, ir, line[:], rel_path, size)

    counter = 0
    for y, line in enumerate(board):
        for x, char in enumerate(line):
            if board[y][x] == "#":
                counter += 1
            print(board[y][x], end="")
        print()
    return counter


def run_IntCode(extended_mem, input_data, ir, line, rel_path, size):
    while ir < size:
        command = line[ir]
        modes, opcode = divmod(command, 100)
        method = opcodes[opcode]
        if method is not None:
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
            if retval == 1:
                retval = "#"
            elif retval == 0:
                retval = "."
            else:
                breakpoint()
    return retval


def sol2(data: str) -> int:
    line = [int(num) for num in data.split(',')]
    ir = 0
    rel_path = 0
    extended_mem = defaultdict(int)
    size = len(line)
    # slope is 1.19 (x = y *1.19)
    min_x = 0
    max_x = 4800
    mid_x = (max_x - min_x) // 2
    mid_y = int(mid_x // 1.19)
    x = None
    y = None
    while min_x + 1 < max_x:
        print(f"{min_x=}, {max_x=}        {mid_x=}, {mid_y=}")
        top_left = run_IntCode(extended_mem, [mid_y, mid_x], ir, line[:], rel_path, size)
        if top_left == ".":
            max_x = mid_x
        else:
            bottom_left = run_IntCode(extended_mem, [mid_y, mid_x + 99], ir, line[:], rel_path, size)
            top_right = run_IntCode(extended_mem, [mid_y + 99, mid_x], ir, line[:], rel_path, size)
            if bottom_left != "#" or top_right != "#":
                min_x = mid_x
            else:
                x = mid_x
                y = mid_y
                max_x = mid_x
        mid_x = (max_x + min_x) // 2
        mid_y = int(mid_x // 1.19)
    assert x is not None
    assert y is not None
    flag = True
    while flag:
        i = 0
        while True:
            i += 1
            x -= 1
            y -= 1
            top_left = run_IntCode(extended_mem, [y, x], ir, line[:], rel_path, size)
            bottom_left = run_IntCode(extended_mem, [y, x + 99], ir, line[:], rel_path, size)
            top_right = run_IntCode(extended_mem, [y + 99, x], ir, line[:], rel_path, size)
            if top_left != "#" or bottom_left != "#" or top_right != "#":
                x += 1
                y += 1
                break
        j = 0
        while True:
            j += 1
            x -= 1
            top_left = run_IntCode(extended_mem, [y, x], ir, line[:], rel_path, size)
            bottom_left = run_IntCode(extended_mem, [y, x + 99], ir, line[:], rel_path, size)
            top_right = run_IntCode(extended_mem, [y + 99, x], ir, line[:], rel_path, size)
            if top_left != "#" or bottom_left != "#" or top_right != "#":
                x += 1
                break
        k = 0
        while True:
            k += 1
            y -= 1
            top_left = run_IntCode(extended_mem, [y, x], ir, line[:], rel_path, size)
            bottom_left = run_IntCode(extended_mem, [y, x + 99], ir, line[:], rel_path, size)
            top_right = run_IntCode(extended_mem, [y + 99, x], ir, line[:], rel_path, size)
            if top_left != "#" or bottom_left != "#" or top_right != "#":
                y += 1
                break
        flag = i != 1 or j != 1 or k != 1
    print(f"{y=}, {x=}")
    return y * 10_000 + x


def get_input(filename: str) -> str:
    with open(filename) as f:
        data = f.read()
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='input.txt')
    args = parser.parse_args()
    data = get_input(args.filename)
    # print(sol1(data))
    print(sol2(data))
    return 0


if __name__ == '__main__':
    exit(main())
