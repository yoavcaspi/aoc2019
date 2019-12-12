import pytest
from day12.solution import sol1, sol2

INPUT_A = """\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""

INPUT_B = """\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"""

@pytest.mark.parametrize('data, input_data, expected',
                         ((INPUT_A, 10, 179),)
                          )
def test_1(data, input_data, expected):
    assert sol1(data, input_data) == expected


@pytest.mark.parametrize('data, expected',
                         ((INPUT_A, 2772),
                          (INPUT_B, 4686774924))
                          )
def test_2(data, expected):
    assert sol2(data) == expected


if __name__ == '__main__':
    pytest.main()
