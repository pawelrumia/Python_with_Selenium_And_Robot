import pytest


def test_divisible_by_3(input_value):
    assert input_value % 3 == 0


def test_divisible_by_6(input_value):
    assert input_value % 6 == 0


@pytest.mark.parametrize("number, result", [(1, 11), (2, 22), (3, 33)])
def test_multiplication(number, result):
    assert 11 * number == result
