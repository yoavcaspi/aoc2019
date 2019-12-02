import pytest
from day2.solution import sol1


@pytest.mark.parametrize('data, expected',
                         (([int(x) for x in '1,0,0,0,99'.split(',')], 2),
                          ([int(x) for x in '2,3,0,3,99'.split(',')], 2),
                          ([int(x) for x in '1,9,10,3,2,3,11,0,99,30,40,50'.split(',')], 3500),
                          ([int(x) for x in '1,1,1,4,99,5,6,0,99'.split(',')], 30),
                          ))
def test_1(data, expected):
    assert sol1(data) == expected


if __name__ == '__main__':
    pytest.main()
