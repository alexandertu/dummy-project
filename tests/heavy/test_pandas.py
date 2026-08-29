"""pandas: frames, grouping, joins, rolling windows."""

import pandas as pd
import pytest

pytestmark = pytest.mark.heavy


@pytest.fixture
def sales() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "region": ["north", "south", "north", "south", "north"],
            "quarter": ["q1", "q1", "q2", "q2", "q3"],
            "revenue": [100.0, 150.0, 120.0, 90.0, 200.0],
        }
    )


def test_frame_shape(sales: pd.DataFrame) -> None:
    assert sales.shape == (5, 3)
    assert list(sales.columns) == ["region", "quarter", "revenue"]


def test_groupby_sum(sales: pd.DataFrame) -> None:
    totals = sales.groupby("region")["revenue"].sum()
    assert totals["north"] == 420.0
    assert totals["south"] == 240.0


def test_merge(sales: pd.DataFrame) -> None:
    managers = pd.DataFrame({"region": ["north", "south"], "manager": ["ada", "grace"]})
    merged = sales.merge(managers, on="region")
    assert len(merged) == len(sales)
    assert set(merged["manager"]) == {"ada", "grace"}


def test_rolling_mean() -> None:
    s = pd.Series(range(100), dtype="float64")
    rolled = s.rolling(window=10).mean()
    assert rolled.isna().sum() == 9
    assert rolled.iloc[-1] == pytest.approx(94.5)


def test_pivot_table(sales: pd.DataFrame) -> None:
    pivot = sales.pivot_table(index="region", columns="quarter", values="revenue", aggfunc="sum")
    assert pivot.loc["north", "q1"] == 100.0
    assert pd.isna(pivot.loc["south", "q3"])
