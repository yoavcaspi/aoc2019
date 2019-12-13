import pytest
from day12.solution import sol1, sol2



@pytest.mark.parametrize('data, input_data, expected',
                         (
                          )
                         )
def test_1(data, input_data, expected):
    assert sol1(data, input_data) == expected


@pytest.mark.parametrize('data, expected',
                         (
                          )
                         )
def test_2(data, expected):
    assert sol2(data) == expected


if __name__ == '__main__':
    pytest.main()
