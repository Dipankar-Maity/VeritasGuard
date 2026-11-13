"""Image validation regression tests for the one canonical screenshot preprocessor."""
import io
import pytest
from PIL import Image
from image_analyzer import prepare_screenshot
from analyzer import InvalidInputError


def _image(fmt="PNG", size=(80, 60), mode="RGB"):
    image = Image.new(mode, size, "blue")
    data = io.BytesIO()
    image.save(data, format=fmt)
    return data.getvalue()


def test_png_and_jpeg_return_clean_jpeg():
    for data in (_image("PNG"), _image("JPEG")):
        result = prepare_screenshot(data)
        assert result.mime_type == "image/jpeg"
        assert result.data.startswith(b"\xff\xd8\xff")
        with Image.open(io.BytesIO(result.data)) as out:
            assert out.getexif() == {}
            assert out.mode == "RGB"


def test_invalid_bytes_rejected():
    with pytest.raises(InvalidInputError):
        prepare_screenshot(b"fake image")


def test_bmp_rejected():
    with pytest.raises(InvalidInputError):
        prepare_screenshot(_image("BMP"))


def test_large_image_downsampled():
    result = prepare_screenshot(_image(size=(3000, 2000)))
    assert max(result.width, result.height) <= 1800


def test_small_image_not_upscaled():
    result = prepare_screenshot(_image(size=(50, 40)))
    assert (result.width, result.height) == (50, 40)
