import pytest
from day18.solution import sol1, sol2

INPUT_A = """\
#########
#b.A.@.a#
#########
"""


INPUT_B = """\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""

INPUT_C = """\
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""

INPUT_D = """\
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""

INPUT_E = """\
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
"""


@pytest.mark.parametrize('data, expected',
                         (
                                 (INPUT_A, 8),
                                 (INPUT_B, 86),
                                 (INPUT_C, 136),
                                 (INPUT_D, 81),
                                 (INPUT_E, 132)
                          )
)
def test_1(data, expected):
    assert sol1(data) == expected


@pytest.mark.parametrize('data, expected',
                         (

                         )
)
def test_2(data, expected):
    assert sol2(data) == expected


if __name__ == '__main__':
    pytest.main()
