"""Functional test demonstrating composed business logic using add and multiply."""

import pytest

from template.arithmetic import add, multiply


@pytest.mark.parametrize(
    ("a", "x", "b", "expected", "test_description"),
    [
        (2, 3, 1, 7, "2*3 + 1 = 7"),
        (0, 5, 3, 3, "zero slope returns offset"),
        (1, 0, 0, 0, "identity at origin"),
        (-1, 4, 10, 6, "negative slope"),
        (0.5, 2.0, 0.5, 1.5, "floating point coefficients"),
    ],
)
def test_linear_combination(a: float, x: float, b: float, expected: float, test_description: str) -> None:
    """Test computing a*x + b by composing multiply and add."""
    result = add(multiply(a, x), b)
    assert result == expected, test_description
