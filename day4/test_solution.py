import pytest
from day4.solution import does_meet_password_criteria, does_meet_password_criteria2


@pytest.mark.parametrize('data, expected',
                         (('111111', True),
                          ('223450', False),
                          ('123789', False),
                          ))
def test_1(data, expected):
    assert does_meet_password_criteria(data) == expected


@pytest.mark.parametrize('data, expected',
                         (('112233', True),
                          ('123444', False),
                          ('111122', True),
                          ))
def test_2(data, expected):
    assert does_meet_password_criteria2(data) == expected


if __name__ == '__main__':
    pytest.main()
