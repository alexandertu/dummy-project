"""pyarrow: columnar tables, compute kernels, Parquet round-trip."""

import io

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pytest

pytestmark = pytest.mark.heavy


@pytest.fixture
def table() -> pa.Table:
    return pa.table(
        {
            "id": pa.array(range(1, 1_001), type=pa.int32()),
            "score": pa.array([float(i % 100) for i in range(1_000)], type=pa.float64()),
            "tag": pa.array(["even" if i % 2 == 0 else "odd" for i in range(1_000)]),
        }
    )


def test_schema(table: pa.Table) -> None:
    assert table.num_rows == 1_000
    assert table.schema.field("id").type == pa.int32()
    assert table.column_names == ["id", "score", "tag"]


def test_compute_sum(table: pa.Table) -> None:
    assert pc.sum(table["id"]).as_py() == 500_500


def test_filter_kernel(table: pa.Table) -> None:
    evens = table.filter(pc.equal(table["tag"], "even"))
    assert evens.num_rows == 500


def test_parquet_roundtrip(table: pa.Table) -> None:
    buf = io.BytesIO()
    pq.write_table(table, buf)
    buf.seek(0)
    restored = pq.read_table(buf)
    assert restored.equals(table)


def test_chunked_array_concat(table: pa.Table) -> None:
    doubled = pa.concat_tables([table, table])
    assert doubled.num_rows == 2_000
    assert pc.sum(doubled["id"]).as_py() == 1_001_000
