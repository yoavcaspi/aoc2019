import pytest
from day10.solution import sol1, sol2


INPUT_A = """\
#####
#..##
#####
#..##
#####
"""

INPUT_B = """\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""


@pytest.mark.parametrize('data, expected',
                         ((INPUT_A, 8),)
)
def test_1(data, expected):
    assert sol1(data) == expected

@pytest.mark.parametrize('data, expected',
                         ((INPUT_B, 802),)
)
def test_2(data, expected):
    assert sol2(data) == expected


if __name__ == '__main__':
    pytest.main()
