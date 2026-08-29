"""Let a pytest-only environment collect the suite.

Every module in this directory imports its library at import time, which is the
point - it is what makes them measure per-worker import cost. But pytest has to
import a module to enumerate it, so in an environment without those libraries
all twelve files raise collection errors, and pytest then exits 2 and reports
nothing. That is fatal for a client like fan-test, which only wants the list of
test IDs and treats a non-zero exit as a collection failure.

Ignoring the files when the libraries are absent turns that into a clean
partial collection: the sleep tests still enumerate, and the exit code is 0.
Note the consequence - the heavy tests are then absent from the list entirely,
so anything dispatching that list will not run them.
"""

import importlib.util

# The full set these tests import at module level, including the ones that are
# a second import inside another file (pandas in test_duckdb, numpy in several).
_LIBRARIES = (
    "duckdb",
    "matplotlib",
    "networkx",
    "numpy",
    "pandas",
    "PIL",
    "polars",
    "pyarrow",
    "scipy",
    "sklearn",
    "statsmodels",
    "sympy",
)

_missing = sorted(name for name in _LIBRARIES if importlib.util.find_spec(name) is None)

# All or nothing: a partial install would otherwise error on whichever file
# imports the one missing library.
collect_ignore_glob = ["test_*.py"] if _missing else []
