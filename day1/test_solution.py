import pytest
from day1.solution import sol1, sol2

@pytest.mark.parametrize('data, expected',
                         ((['12'], 2),
                          (['14'], 2),
                          (['1969'], 654),
                          (['100756'], 33583),
                          ))
def test_1(data, expected):
    assert sol1(data) == expected


@pytest.mark.parametrize('data, expected',
                         ((['12'], 2),
                          (['14'], 2),
                          (['1969'], 966),
                          (['100756'], 50346),
                          ))
def test_2(data, expected):
    assert sol2(data) == expected


if __name__ == '__main__':
    pytest.main()
