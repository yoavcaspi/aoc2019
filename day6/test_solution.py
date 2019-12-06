import pytest
from day6.solution import sol1, sol2

@pytest.mark.parametrize('data, expected',
                         (([
                                "COM)B",
                                "B)C",
                                "C)D",
                                "D)E",
                                "E)F",
                                "B)G",
                                "G)H",
                                "D)I",
                                "E)J",
                                "J)K",
                                "K)L",
                           ], 42),

                          ))
def test_1(data, expected):
    assert sol1(data) == expected


@pytest.mark.parametrize('data, expected',
                         (([
                                "COM)B",
                                "B)C",
                                "C)D",
                                "D)E",
                                "E)F",
                                "B)G",
                                "G)H",
                                "D)I",
                                "E)J",
                                "J)K",
                                "K)L",
                                "K)YOU",
                                "I)SAN",
                           ], 4),

                          ))
def test_2(data, expected):
    assert sol2(data) == expected


if __name__ == '__main__':
    pytest.main()
