"""Suite 102: 10 tests, each burning ~0.3s of CPU on the reference machine."""

from _workload import burn

ITERATIONS = 5250000


def test_case_01() -> None:
    assert burn(ITERATIONS) >= 0


def test_case_02() -> None:
    assert burn(ITERATIONS) >= 0


def test_case_03() -> None:
    assert burn(ITERATIONS) >= 0


def test_case_04() -> None:
    assert burn(ITERATIONS) >= 0


def test_case_05() -> None:
    assert burn(ITERATIONS) >= 0


def test_case_06() -> None:
    assert burn(ITERATIONS) >= 0


def test_case_07() -> None:
    assert burn(ITERATIONS) >= 0


def test_case_08() -> None:
    assert burn(ITERATIONS) >= 0


def test_case_09() -> None:
    assert burn(ITERATIONS) >= 0


def test_case_10() -> None:
    assert burn(ITERATIONS) >= 0
