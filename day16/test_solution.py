import pytest
from day16.solution import sol1, sol2


@pytest.mark.parametrize('data, phases, expected',
                         (
                            ("12345678", 4, "01029498"),
                            ("80871224585914546619083218645595", 100, "24176176"),
                            ("19617804207202209144916044189917", 100, "73745418"),
                            ("69317163492948606335995924319873", 100, "52432133"),
                          )
)
def test_1(data, phases, expected):
    assert sol1(data, phases=phases) == expected


@pytest.mark.parametrize('data, expected',
                         (
                                 ("03036732577212944063491565474664", "84462026"),
                                 ("02935109699940807407585447034323", "78725270"),
                                 ("03081770884921959731165446850517", "53553731"),
                         )
)
def test_2(data, expected):
    assert sol2(data) == expected


if __name__ == '__main__':
    pytest.main()
