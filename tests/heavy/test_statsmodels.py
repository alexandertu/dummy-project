"""statsmodels: ordinary least squares and its diagnostics."""

import numpy as np
import pytest
import statsmodels.api as sm

pytestmark = pytest.mark.heavy


@pytest.fixture
def fitted():
    rng = np.random.default_rng(seed=99)
    x = rng.uniform(0.0, 10.0, size=500)
    y = 3.0 * x + 7.0 + rng.normal(scale=0.5, size=500)
    return sm.OLS(y, sm.add_constant(x)).fit()


def test_recovers_slope_and_intercept(fitted) -> None:
    intercept, slope = fitted.params
    assert intercept == pytest.approx(7.0, abs=0.15)
    assert slope == pytest.approx(3.0, abs=0.05)


def test_r_squared_is_high(fitted) -> None:
    assert fitted.rsquared > 0.99


def test_slope_is_significant(fitted) -> None:
    assert fitted.pvalues[1] < 1e-10


def test_prediction(fitted) -> None:
    predicted = fitted.predict(sm.add_constant(np.array([0.0, 10.0])))
    assert predicted[0] == pytest.approx(7.0, abs=0.2)
    assert predicted[1] == pytest.approx(37.0, abs=0.3)


def test_residuals_centre_on_zero(fitted) -> None:
    assert fitted.resid.mean() == pytest.approx(0.0, abs=1e-9)
    assert len(fitted.resid) == 500
