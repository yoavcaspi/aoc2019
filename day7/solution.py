import argparse
from typing import List, Dict, Optional
from itertools import permutations


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
        data[vals[0]] = input_data.pop(0)
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


def sol1(data: List[int]) -> int:
    max_output = -1
    for permute in permutations((4, 3, 2, 1, 0)):
        output = 0
        for i in range(5):
            amp_data = data[:]
            input_data = [permute[i], output]
            ir = 0
            while ir < len(amp_data):
                command = amp_data[ir]
                modes, opcode = divmod(command, 100)
                method = opcodes[opcode]
                if method is not None:
                    output = method.run(input_data, amp_data, modes, *amp_data[ir + 1:ir + method.instruction_size])
                else:
                    break
                if isinstance(method, ConditionalJump) and output:
                    ir = method.get_new_ip()
                else:
                    ir += method.instruction_size
                if not isinstance(method, ConditionalJump) and output is not None:
                    print(output)
        max_output = max(max_output, output)
    return max_output


def sol2(data: List[int]) -> int:
    max_output = -1
    for permute in permutations((9, 8, 7, 6, 5)):
        output = 0
        amp_data = [data[:], data[:], data[:], data[:], data[:]]
        input_data = [[permute[0], 0], [permute[1]], [permute[2]], [permute[3]], [permute[4]]]
        ir = [0] * 5
        i = 0
        while True:
            output, was_stopped, ir[i % 5] = compute(amp_data[i % 5], input_data[i % 5], ir[i % 5])
            input_data[(i + 1) % 5].append(output)
            if was_stopped and i % 5 == 4:
                break
            i += 1
        max_output = max(max_output, output)
    return max_output


def compute(amp_data, input_data, ir):
    was_stopped = False
    retval = None
    while ir < len(amp_data):
        command = amp_data[ir]
        modes, opcode = divmod(command, 100)
        method = opcodes[opcode]
        if isinstance(method, Input) and len(input_data) == 0:
            return retval, was_stopped, ir
        if method is not None:
            output = method.run(input_data, amp_data, modes, *amp_data[ir + 1:ir + method.instruction_size])
        else:
            was_stopped = True
            break
        if isinstance(method, ConditionalJump) and output:
            ir = method.get_new_ip()
        else:
            ir += method.instruction_size
        if isinstance(method, Output):
            retval = output
        if not isinstance(method, ConditionalJump) and output is not None:
            print(output)
    return retval, was_stopped, ir


def get_input(filename: str) -> List[str]:
    with open(filename) as f:
        lines = f.readlines()
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='input.txt')
    args = parser.parse_args()
    data = get_input(args.filename)
    new_data = [int(x) for x in data[0].split(',')]
    print(sol1(new_data))
    print(sol2(new_data))
    return 0


if __name__ == '__main__':
    exit(main())
