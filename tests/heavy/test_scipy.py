"""scipy: optimisation, integration, sparse matrices, statistics."""

import numpy as np
import pytest
from scipy import integrate, optimize, sparse, stats

pytestmark = pytest.mark.heavy


def test_minimize_scalar() -> None:
    result = optimize.minimize_scalar(lambda x: (x - 3.0) ** 2 + 1.0)
    assert result.success
    assert result.x == pytest.approx(3.0, abs=1e-5)


def test_quad_integration() -> None:
    area, error = integrate.quad(np.sin, 0.0, np.pi)
    assert area == pytest.approx(2.0, abs=1e-8)
    assert error < 1e-8


def test_sparse_matrix() -> None:
    m = sparse.csr_matrix(np.eye(500))
    assert m.nnz == 500
    assert (m @ np.ones(500)).sum() == pytest.approx(500.0)


def test_ttest_of_identical_samples() -> None:
    rng = np.random.default_rng(seed=7)
    a = rng.normal(size=2_000)
    result = stats.ttest_ind(a, a)
    assert result.pvalue == pytest.approx(1.0)


def test_root_finding() -> None:
    root = optimize.brentq(lambda x: x**2 - 2.0, 0.0, 2.0)
    assert root == pytest.approx(np.sqrt(2.0))
