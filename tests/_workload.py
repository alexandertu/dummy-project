"""The CPU workload the suite is built from.

Earlier versions of these tests slept. That measured scheduling, which is a
real thing to measure, but it could not tell two kinds of parallelism apart:
`time.sleep()` uses no CPU, so `pytest -n 50` on a 4-core runner overlaps fifty
sleeping processes happily and looked nearly as fast as fifty remote sandboxes.
No real suite behaves that way.

Work that actually occupies a core does not overlap. In-process parallelism
saturates at the machine's core count however high `-n` goes, while a
distributed runner keeps scaling because every shard gets its own machine. That
difference is the whole question, and it only appears under real load.

The loop is pure Python on purpose - no numpy, no hashlib - so it holds the GIL
and cannot be quietly vectorised or handed to a C library that releases it.
Work is expressed in iterations rather than seconds because a fixed duration
would mean different amounts of work on different hardware, and comparing
hardware is the point.
"""

#: Iterations per second on the machine that generated these tests (~17.5M/s).
#: A slower machine takes proportionally longer: the work is fixed, not the time.
ITERATIONS_PER_SECOND = 17_500_000


def burn(iterations: int) -> int:
    """Occupy a core deterministically, returning a value that cannot be elided."""
    total = 0
    for i in range(iterations):
        total = (total * 31 + i) % 1000003
    return total
