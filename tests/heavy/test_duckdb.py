"""duckdb: in-process SQL over literals and dataframes."""

import duckdb
import pandas as pd
import pytest

pytestmark = pytest.mark.heavy


@pytest.fixture
def con():
    connection = duckdb.connect(":memory:")
    yield connection
    connection.close()


def test_scalar_query(con) -> None:
    assert con.execute("SELECT 6 * 7").fetchone()[0] == 42


def test_generate_series(con) -> None:
    total = con.execute("SELECT sum(i) FROM generate_series(1, 100) AS t(i)").fetchone()[0]
    assert total == 5050


def test_group_by(con) -> None:
    con.execute("CREATE TABLE events (kind VARCHAR, weight INTEGER)")
    con.execute("INSERT INTO events VALUES ('a', 1), ('b', 2), ('a', 3), ('b', 4)")
    rows = con.execute("SELECT kind, sum(weight) FROM events GROUP BY kind ORDER BY kind").fetchall()
    assert rows == [("a", 4), ("b", 6)]


def test_query_a_pandas_frame(con) -> None:
    frame = pd.DataFrame({"n": range(1, 11)})  # noqa: F841 — duckdb resolves it by name
    result = con.execute("SELECT avg(n) FROM frame").fetchone()[0]
    assert result == pytest.approx(5.5)


def test_join(con) -> None:
    con.execute("CREATE TABLE l (id INTEGER, name VARCHAR)")
    con.execute("CREATE TABLE r (id INTEGER, score INTEGER)")
    con.execute("INSERT INTO l VALUES (1, 'x'), (2, 'y')")
    con.execute("INSERT INTO r VALUES (1, 10), (2, 20)")
    rows = con.execute("SELECT l.name, r.score FROM l JOIN r USING (id) ORDER BY l.id").fetchall()
    assert rows == [("x", 10), ("y", 20)]
