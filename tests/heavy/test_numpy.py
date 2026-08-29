"""numpy: arrays, linear algebra, statistics."""

import numpy as np
import pytest

pytestmark = pytest.mark.heavy


def test_array_sum() -> None:
    assert np.arange(101).sum() == 5050


def test_dot_product() -> None:
    a, b = np.array([1.0, 2.0, 3.0]), np.array([4.0, 5.0, 6.0])
    assert np.dot(a, b) == pytest.approx(32.0)


def test_broadcasting() -> None:
    grid = np.arange(3).reshape(3, 1) + np.arange(4).reshape(1, 4)
    assert grid.shape == (3, 4)
    assert grid[2, 3] == 5


def test_descriptive_stats() -> None:
    rng = np.random.default_rng(seed=1234)
    sample = rng.normal(loc=10.0, scale=2.0, size=50_000)
    assert sample.mean() == pytest.approx(10.0, abs=0.05)
    assert sample.std() == pytest.approx(2.0, abs=0.05)


def test_linalg_solve() -> None:
    a = np.array([[3.0, 1.0], [1.0, 2.0]])
    x = np.linalg.solve(a, np.array([9.0, 8.0]))
    assert np.allclose(a @ x, [9.0, 8.0])
