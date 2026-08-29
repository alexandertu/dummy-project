# dummy-project

A synthetic pytest suite for exercising test runners. There is no application
code here. The suite measures the *runner*, in two independent dimensions:

| Suite | What it costs | What it measures |
| --- | --- | --- |
| **sleep tests** (100, unmarked) | ~102 s wall clock, ~0 CPU | scheduling, sharding, wall-clock distribution |
| **heavy tests** (60, `heavy` marker) | ~2 s warm, ~42 s in a fresh env | dependency install and per-worker import cost |

## Install

Dependencies are installed with **pip**, not uv, deliberately — pip resolves and
downloads serially, which is the slower and more representative cold-start cost.
`--no-cache-dir` stops pip reusing a warm wheel cache, so every install pays the
full download:

```sh
python3 -m venv .venv
./.venv/bin/pip install --no-cache-dir -r requirements.txt
```

`requirements.txt` holds the unpinned top level; `requirements.lock.txt` is a
`pip freeze` of a known-good resolution if you need runs to be comparable.

Measured on one machine, one fast connection: **21 s**, 34 packages, **886 MB**
on disk. Expect that to move a lot with link speed — it is download-bound, not
CPU-bound.

## The sleep tests

100 tests across `tests/test_suite_01.py` … `tests/test_suite_10.py`, each
holding `test_case_01` … `test_case_10`. Every body is a bare `time.sleep()`.
All ten tests in a file sleep the same amount; the amount climbs file to file:

| File | Sleep per test | File total |
| --- | --- | --- |
| `test_suite_01.py` | 0.1s | 1.0s |
| `test_suite_02.py` | 0.3s | 3.0s |
| `test_suite_03.py` | 0.5s | 5.0s |
| `test_suite_04.py` | 0.7s | 7.0s |
| `test_suite_05.py` | 0.9s | 9.0s |
| `test_suite_06.py` | 1.1s | 11.0s |
| `test_suite_07.py` | 1.3s | 13.0s |
| `test_suite_08.py` | 1.5s | 15.0s |
| `test_suite_09.py` | 1.8s | 18.0s |
| `test_suite_10.py` | 2.0s | 20.0s |

Serial total: **~102 s**. The durations are deliberately uneven, so an even
split of files or tests across workers does *not* produce an even split of
wall-clock time — the point, if you are testing shard balancing.

## The heavy tests

60 tests across 12 files in `tests/heavy/`, one file per library. Each imports
its library at module level and runs small but real operations with real
assertions, so the suite doubles as an install smoke test — if a wheel is
broken or missing, these fail rather than silently passing.

`numpy` · `scipy` · `pandas` · `scikit-learn` · `matplotlib` · `pillow` ·
`pyarrow` · `polars` · `duckdb` · `networkx` · `sympy` · `statsmodels`

The compute is trivial. The cost is getting the libraries into memory:

- **~1.3 s** of warm imports per worker process — mostly `scikit-learn` (430 ms),
  `statsmodels` (280 ms), `pandas` (160 ms), `sympy` (140 ms).
- **~40 s extra on the first run in a fresh environment** — matplotlib scanning
  the system fonts to build its cache, plus bytecode compilation of the
  installed packages. A cold container pays this once; a warm one never does.
  It is easy to mistake for slow tests, so measure the second run too.

## Running

```sh
./.venv/bin/python -m pytest                    # everything: ~104 s
./.venv/bin/python -m pytest -m "not heavy"     # sleep baseline only: ~102 s
./.venv/bin/python -m pytest -m heavy           # dependency tests only: ~2 s warm
```

Every test passes. The sleep tests assert nothing; the heavy tests assert real
properties of real libraries.

## CI

`.github/workflows/tests.yml` runs the full suite on every push and pull
request, on `ubuntu-latest` and the Python in `.python-version`. It writes a
job summary with the cold install time, the sleep/heavy split and per-file
totals, and uploads the JUnit XML as a build artifact.

It deliberately does **not** cache pip. Caching would make CI faster and hide
the number this repo exists to measure. If you would rather have quick CI, add
`cache: pip` to the `setup-python` step and drop `--no-cache-dir`.
