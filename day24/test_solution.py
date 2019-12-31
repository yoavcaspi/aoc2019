import pytest
from day24.solution import sol1, sol2

INPUT_A = """\
....#
#..#.
#..##
..#..
#....
"""


@pytest.mark.parametrize('data, expected',
                         (
                                 (INPUT_A, 2129920),
                         )
                         )
def test_1(data, expected):
    assert sol1(data) == expected


@pytest.mark.parametrize('data, num_minutes, expected',
                         (
                                 (INPUT_A, 10, 99),
                         )
                         )
def test_2(data, num_minutes, expected):
    assert sol2(data, num_minutes) == expected


if __name__ == '__main__':
    pytest.main()
