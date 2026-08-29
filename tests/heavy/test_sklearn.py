"""scikit-learn: preprocessing, regression, clustering, model selection."""

import numpy as np
import pytest
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

pytestmark = pytest.mark.heavy


@pytest.fixture
def linear_data() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed=42)
    x = rng.uniform(-5.0, 5.0, size=(400, 1))
    y = 2.5 * x.ravel() + 1.0 + rng.normal(scale=0.1, size=400)
    return x, y


def test_linear_regression_recovers_coefficients(linear_data) -> None:
    x, y = linear_data
    model = LinearRegression().fit(x, y)
    assert model.coef_[0] == pytest.approx(2.5, abs=0.05)
    assert model.intercept_ == pytest.approx(1.0, abs=0.05)


def test_r2_on_held_out_split(linear_data) -> None:
    x, y = linear_data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)
    model = LinearRegression().fit(x_train, y_train)
    assert r2_score(y_test, model.predict(x_test)) > 0.99


def test_standard_scaler_centres_and_scales() -> None:
    rng = np.random.default_rng(seed=3)
    scaled = StandardScaler().fit_transform(rng.normal(loc=50.0, scale=7.0, size=(1_000, 3)))
    assert np.allclose(scaled.mean(axis=0), 0.0, atol=1e-9)
    assert np.allclose(scaled.std(axis=0), 1.0, atol=1e-9)


def test_kmeans_separates_two_blobs() -> None:
    rng = np.random.default_rng(seed=11)
    blobs = np.vstack([rng.normal(-8.0, 0.4, (150, 2)), rng.normal(8.0, 0.4, (150, 2))])
    labels = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(blobs)
    assert len(set(labels)) == 2
    # Every point in a blob should land in the same cluster.
    assert len(set(labels[:150])) == 1
    assert len(set(labels[150:])) == 1


def test_train_test_split_sizes(linear_data) -> None:
    x, y = linear_data
    x_train, x_test, _, _ = train_test_split(x, y, test_size=0.2, random_state=0)
    assert len(x_train) == 320
    assert len(x_test) == 80
