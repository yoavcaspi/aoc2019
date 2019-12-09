import pytest
from day9.part1 import sol as part1_sol


@pytest.mark.parametrize('data, expected',
                         (('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99',
                           '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'),
                          ("1102,34915192,34915192,7,4,7,99,0", 1_219_070_632_396_864),
                          ("104,1125899906842624,99", 1125899906842624),
                          ))
def test_part1(data, expected):
    assert part1_sol(data) == expected


if __name__ == '__main__':
    pytest.main()
