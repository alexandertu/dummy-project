"""sympy: symbolic algebra and calculus."""

import pytest
import sympy as sp

pytestmark = pytest.mark.heavy

x, y = sp.symbols("x y")


def test_expand() -> None:
    assert sp.expand((x + 1) ** 3) == x**3 + 3 * x**2 + 3 * x + 1


def test_factor() -> None:
    assert sp.factor(x**2 - y**2) == (x - y) * (x + y)


def test_solve_quadratic() -> None:
    assert sorted(sp.solve(x**2 - 5 * x + 6, x)) == [2, 3]


def test_derivative() -> None:
    assert sp.diff(sp.sin(x) * x, x) == sp.sin(x) + x * sp.cos(x)


def test_definite_integral() -> None:
    assert sp.integrate(sp.sin(x), (x, 0, sp.pi)) == 2
