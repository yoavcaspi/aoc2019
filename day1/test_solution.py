import pytest
from day1.solution import sol1

@pytest.mark.parametrize('data, expected',
                         ((['12'], 2),
                          (['14'], 2),
                          (['1969'], 654),
                          (['100756'], 33583),
                          ))
def test_1(data, expected):
    assert sol1(data) == expected


if __name__ == '__main__':
    pytest.main()
