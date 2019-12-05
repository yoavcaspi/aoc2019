import argparse
from typing import List, Dict, Any, Optional


class Opcode:
    def __init__(self):
        self.instruction_size = 0

    def run(self, input_data: List[int], data: List[int], modes: int, *vals) -> Optional[int]:
        raise NotImplemented()


class Operand(Opcode):
    pass


class Add(Operand):
    def __init__(self):
        super().__init__()
        self.instruction_size = 4

    def run(self, input_data: List[int], data: List[int], modes: int, *vals) -> Optional[int]:
        assert len(vals) == 3
        retval = 0
        for i in range(self.instruction_size - 2):
            modes, mode = divmod(modes, 10)
            if mode == 0:
                retval += data[vals[i]]
            else:
                retval += vals[i]
        data[vals[2]] = retval
        return None


class Mul(Operand):
    def __init__(self):
        super().__init__()
        self.instruction_size = 4

    def run(self, input_data: List[int], data: List[int], modes: int, *vals) -> Optional[int]:
        assert len(vals) == 3
        retval = 1
        for i in range(self.instruction_size - 2):
            modes, mode = divmod(modes, 10)
            if mode == 0:
                retval *= data[vals[i]]
            else:
                retval *= vals[i]
        data[vals[2]] = retval
        return None


class Io(Opcode):
    pass


class Input(Io):
    def __init__(self):
        super().__init__()
        self.instruction_size = 2

    def run(self, input_data: List[int], data: List[int], modes: int, *vals) -> Optional[int]:
        assert len(vals) == 1
        data[vals[0]] = input_data[0]
        return None


class Output(Io):
    def __init__(self):
        super().__init__()
        self.instruction_size = 2

    def run(self, input_data: List[int], data: List[int], modes: int, *vals) -> Optional[int]:
        assert len(vals) == 1
        if modes == 0:
            return data[vals[0]]
        else:
            return vals[0]
        return


class ConditionalJump(Opcode):
    def __init__(self):
        super().__init__()
        self.instruction_size = 3
        self.jump_to = -1

    def run(self, input_data: List[int], data: List[int], modes: int, *vals) -> Optional[int]:
        val: int = 0
        modes, mode = divmod(modes, 10)
        if mode == 0:
            val = data[vals[0]]
        else:
            val = vals[0]
        modes, mode = divmod(modes, 10)
        self.jump_to = vals[1] if mode else data[vals[1]]
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

    def run(self, input_data: List[int], data: List[int], modes: int, *vals) -> Optional[int]:
        modes, mode = divmod(modes, 10)
        if mode == 0:
            val1 = data[vals[0]]
        else:
            val1 = vals[0]

        modes, mode = divmod(modes, 10)
        if mode == 0:
            val2 = data[vals[1]]
        else:
            val2 = vals[1]
        address = vals[2]

        if self.condition(val1, val2):
            data[address] = 1
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


opcodes: Dict[int, Opcode] = dict(
    ((1, Add()),
     (2, Mul()),
     (3, Input()),
     (4, Output()),
     (5, JumpIfTrue()),
     (6, JumpIfFalse()),
     (7, LessThan()),
     (8, Equals()),
     (99, None)))


def sol1(data: List[List[int]], input_data: List[int]) -> int:
    for line in data:
        i = 0
        size = len(line)
        while i < size:
            command = line[i]
            modes, opcode = divmod(command, 100)
            method = opcodes[opcode]
            if method is not None:
                retval = method.run(input_data, line, modes, *line[i + 1:i + method.instruction_size])
            else:
                break
            i += method.instruction_size
            if retval is not None:
                print(retval)
    return retval


def sol2(data: List[List[int]], input_data: List[int]) -> int:
    retval2 = None
    for line in data:
        i = 0
        size = len(line)
        while i < size:
            command = line[i]
            modes, opcode = divmod(command, 100)
            method = opcodes[opcode]
            if method is not None:
                retval = method.run(input_data, line, modes, *line[i + 1:i + method.instruction_size])
            else:
                break
            if isinstance(method, ConditionalJump) and retval:
                i = method.get_new_ip()
            else:
                i += method.instruction_size
            if not isinstance(method, ConditionalJump) and retval is not None:
                print(retval)
                retval2 = retval
    return retval2


def get_input(filename: str) -> List[str]:
    with open(filename) as f:
        lines = f.readlines()
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='input.txt')
    args = parser.parse_args()
    data = get_input(args.filename)
    new_data = []
    for line in data:
        new_data.append([int(x) for x in line.split(',')])
    print(sol1(new_data, [1]))
    new_data = []
    for line in data:
        new_data.append([int(x) for x in line.split(',')])

    print(sol2(new_data, [5]))
    return 0


if __name__ == '__main__':
    exit(main())
