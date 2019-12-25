import pytest
from day22.solution import sol1, sol2

INPUT_A = """\
deal with increment 7
deal into new stack
deal into new stack
"""

INPUT_B = """\
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""

INPUT_C = """\
deal with increment 7
deal with increment 9
cut -2
"""


@pytest.mark.parametrize('data, size, expected',
                         (
                                 (INPUT_A, 10, "0 3 6 9 2 5 8 1 4 7"),
                                 (INPUT_B, 10, "9 2 5 8 1 4 7 0 3 6"),
                                 (INPUT_C, 10, "6 3 0 7 4 1 8 5 2 9"),

                         )
                         )
def test_1(data, size, expected):
    assert sol1(data, size) == expected


@pytest.mark.parametrize('data, size, pos, expected',
                         (
                                 (INPUT_A, 10, 4, "0 3 6 9 2 5 8 1 4 7"),
                                 (INPUT_B, 10, 4, "9 2 5 8 1 4 7 0 3 6"),
                                 (INPUT_C, 10, 4, "6 3 0 7 4 1 8 5 2 9"),
                         )
                         )
def test_2(data, size, pos, expected):
    assert sol2(data, size, pos) == expected


if __name__ == '__main__':
    pytest.main()
