import argparse
from typing import List, Dict, Any, Optional


class Opcode:
    def __init__(self):
        self.instruction_size = 0

    def run(self, input_data: List[int], data: List[int], modes: int, *vals) -> Optional[int]:
        raise NotImplemented()


class Add(Opcode):
    def __init__(self):
        super().__init__()
        self.instruction_size = 4

    def run(self, input_data: List[int], data: List[int], modes: int, *vals) -> Optional[int]:
        assert len(vals) == 3
        retval = 0
        for i in range(2):
            modes, mode = divmod(modes, 10)
            if mode == 0:
                retval += data[vals[i]]
            else:
                retval += vals[i]
        data[vals[2]] = retval
        return None


class Mul(Opcode):
    def __init__(self):
        super().__init__()
        self.instruction_size = 4

    def run(self, input_data: List[int], data: List[int], modes: int, *vals) -> Optional[int]:
        assert len(vals) == 3
        retval = 1
        for i in range(2):
            modes, mode = divmod(modes, 10)
            if mode == 0:
                retval *= data[vals[i]]
            else:
                retval *= vals[i]
        data[vals[2]] = retval
        return None


class Input(Opcode):
    def __init__(self):
        super().__init__()
        self.instruction_size = 2

    def run(self, input_data: List[int], data: List[int], modes: int, *vals) -> Optional[int]:
        assert len(vals) == 1
        data[vals[0]] = input_data[0]
        return None


class Output(Opcode):
    def __init__(self):
        super().__init__()
        self.instruction_size = 2

    def run(self, input_data: List[int], data: List[int], modes: int, *vals) -> Optional[int]:
        assert len(vals) == 1
        return data[vals[0]]


opcodes: Dict[int, Opcode] = dict(((1, Add()), (2, Mul()), (3, Input()), (4, Output()), (99, None)))


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


def sol2(data: List[str]) -> int:
    expected_data = 19690720
    for noun in range(100):
        for verb in range(100):
            new_data = [int(x) for x in data[0].split(',')]
            new_data[1] = noun
            new_data[2] = verb
            if expected_data == sol1(new_data):
                return 100 * noun + verb
    return -1


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
    # print(sol2(data))
    return 0


if __name__ == '__main__':
    exit(main())
