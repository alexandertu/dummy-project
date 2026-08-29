"""pillow: image creation and transforms."""

import io

import pytest
from PIL import Image

pytestmark = pytest.mark.heavy


@pytest.fixture
def swatch() -> Image.Image:
    return Image.new("RGB", (320, 240), color=(42, 120, 214))


def test_size_and_mode(swatch: Image.Image) -> None:
    assert swatch.size == (320, 240)
    assert swatch.mode == "RGB"
    assert swatch.getpixel((0, 0)) == (42, 120, 214)


def test_resize(swatch: Image.Image) -> None:
    small = swatch.resize((80, 60), Image.Resampling.LANCZOS)
    assert small.size == (80, 60)


def test_rotate_swaps_axes(swatch: Image.Image) -> None:
    turned = swatch.rotate(90, expand=True)
    assert turned.size == (240, 320)


def test_greyscale_conversion(swatch: Image.Image) -> None:
    grey = swatch.convert("L")
    assert grey.mode == "L"
    assert isinstance(grey.getpixel((10, 10)), int)


def test_png_roundtrip(swatch: Image.Image) -> None:
    buf = io.BytesIO()
    swatch.save(buf, format="PNG")
    buf.seek(0)
    reopened = Image.open(buf)
    assert reopened.format == "PNG"
    assert reopened.size == swatch.size
