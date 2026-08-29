"""matplotlib: figure construction and PNG rendering on the Agg backend."""

import io

import matplotlib
import pytest

matplotlib.use("Agg")  # headless: no GUI toolkit in a test runner

import matplotlib.pyplot as plt  # noqa: E402  (must follow the backend choice)

pytestmark = pytest.mark.heavy


@pytest.fixture
def figure():
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    yield fig, ax
    plt.close(fig)


def test_backend_is_headless() -> None:
    assert matplotlib.get_backend().lower() == "agg"


def test_figure_dimensions(figure) -> None:
    fig, _ = figure
    assert fig.get_size_inches() == pytest.approx([4.0, 3.0])
    assert fig.dpi == 100


def test_line_plot_keeps_its_data(figure) -> None:
    _, ax = figure
    (line,) = ax.plot([0, 1, 2, 3], [0, 1, 4, 9])
    assert line.get_xydata().shape == (4, 2)
    assert ax.get_lines()[0] is line


def test_renders_a_real_png(figure) -> None:
    fig, ax = figure
    ax.plot(range(50), [v**0.5 for v in range(50)])
    ax.set_title("sqrt")
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    # PNG magic number: the render actually produced an image.
    assert buf.getvalue()[:8] == b"\x89PNG\r\n\x1a\n"
    assert buf.tell() > 1_000


def test_colormap_lookup() -> None:
    viridis = matplotlib.colormaps["viridis"]
    assert viridis(0.0) != viridis(1.0)
    assert len(viridis(0.5)) == 4
