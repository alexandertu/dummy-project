"""polars: eager frames, expressions, joins, lazy execution."""

import polars as pl
import pytest

pytestmark = pytest.mark.heavy


@pytest.fixture
def orders() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "customer": ["ada", "grace", "ada", "linus", "grace"],
            "amount": [10.0, 25.0, 15.0, 40.0, 5.0],
            "status": ["paid", "paid", "pending", "paid", "pending"],
        }
    )


def test_shape_and_dtypes(orders: pl.DataFrame) -> None:
    assert orders.shape == (5, 3)
    assert orders.schema["amount"] == pl.Float64


def test_filter(orders: pl.DataFrame) -> None:
    paid = orders.filter(pl.col("status") == "paid")
    assert paid.height == 3
    assert paid["amount"].sum() == pytest.approx(75.0)


def test_group_by_aggregate(orders: pl.DataFrame) -> None:
    totals = orders.group_by("customer").agg(pl.col("amount").sum().alias("total")).sort("customer")
    assert totals.to_dicts() == [
        {"customer": "ada", "total": 25.0},
        {"customer": "grace", "total": 30.0},
        {"customer": "linus", "total": 40.0},
    ]


def test_join(orders: pl.DataFrame) -> None:
    tiers = pl.DataFrame({"customer": ["ada", "grace", "linus"], "tier": ["gold", "silver", "gold"]})
    joined = orders.join(tiers, on="customer", how="left")
    assert joined.height == orders.height
    assert set(joined["tier"].unique()) == {"gold", "silver"}


def test_lazy_execution(orders: pl.DataFrame) -> None:
    plan = orders.lazy().filter(pl.col("amount") > 10.0).select(pl.col("amount").mean())
    assert plan.collect().item() == pytest.approx((25.0 + 15.0 + 40.0) / 3)
