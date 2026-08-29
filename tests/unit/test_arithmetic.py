import pytest

from package_name.arithmetic import add, multiply


@pytest.mark.parametrize(
    ("a", "b", "expected", "test_description"),
    [
        (1, 2, 3, "positive integers"),
        (-1, 1, 0, "negative and positive cancel out"),
        (0, 0, 0, "zeros"),
        (1.5, 2.5, 4.0, "floating point numbers"),
    ],
)
def test_add(a: float, b: float, expected: float, test_description: str) -> None:
    assert add(a, b) == expected, test_description


@pytest.mark.parametrize(
    ("a", "b", "expected", "test_description"),
    [
        (2, 3, 6, "positive integers"),
        (-2, 3, -6, "negative times positive"),
        (0, 5, 0, "multiply by zero"),
        (1.5, 2.0, 3.0, "floating point numbers"),
    ],
)
def test_multiply(a: float, b: float, expected: float, test_description: str) -> None:
    assert multiply(a, b) == expected, test_description
