"""No-network screenshot tests; Gemini is always mocked."""

from io import BytesIO
from unittest.mock import MagicMock

import pytest
from PIL import Image
from google.genai.errors import APIError

from analyzer import (
    FraudAnalysisError, InvalidInputError, QuotaExceededError,
    ServiceUnavailableError,
)
from image_analyzer import (
    MAX_UPLOAD_BYTES, MAX_SIDE_PIXELS, analyze_screenshot, prepare_screenshot,
)
from schema import RiskLevel


def make_image(fmt="PNG", size=(1800, 800), mode="RGB"):
    image = Image.new(mode, size, "red" if mode == "RGB" else (255, 0, 0, 90))
    buf = BytesIO()
    image.save(buf, fmt)
    return buf.getvalue()


def fake_api_response():
    resp = MagicMock()
    resp.text = """{
      "risk_level": "Critical",
      "scam_category": "Bank/KYC Impersonation",
      "deceptive_tactics": ["OTP request"],
      "psychological_manipulation": ["Fear"],
      "plain_language_explanation": "Suspicious request to share OTP.",
      "protective_actions": ["Do not share OTP"],
      "safety_disclaimer": "This is an automated estimate, not verification."
    }"""
    return resp


def test_png_is_accepted_and_converted_to_metadata_free_jpeg():
    screenshot = prepare_screenshot(make_image())
    assert screenshot.mime_type == "image/jpeg"
    assert screenshot.data[:3] == b"\xff\xd8\xff"
    assert screenshot.width == 1800
    with Image.open(BytesIO(screenshot.data)) as saved:
        assert saved.format == "JPEG"
        assert saved.getexif() == {}


def test_jpeg_is_accepted():
    prepared = prepare_screenshot(make_image(fmt="JPEG"))
    assert prepared.mime_type == "image/jpeg"


def test_transparency_composited_on_white():
    prepared = prepare_screenshot(make_image(size=(100, 100), mode="RGBA"))
    with Image.open(BytesIO(prepared.data)) as saved:
        assert saved.mode == "RGB"


def test_large_image_is_downscaled():
    prepared = prepare_screenshot(make_image(size=(3600, 1800)))
    assert max(prepared.width, prepared.height) <= MAX_SIDE_PIXELS


def test_empty_corrupt_and_unsupported_are_rejected():
    with pytest.raises(InvalidInputError):
        prepare_screenshot(b"")
    with pytest.raises(InvalidInputError):
        prepare_screenshot(b"not a picture")
    with pytest.raises(InvalidInputError):
        prepare_screenshot(make_image(fmt="GIF"))


def test_oversize_file_rejected_without_image_decoding():
    with pytest.raises(InvalidInputError, match="maximum 8 MB"):
        prepare_screenshot(b"A" * (MAX_UPLOAD_BYTES + 1))


def test_pixel_bomb_is_rejected():
    with pytest.raises(InvalidInputError):
        prepare_screenshot(make_image(size=(5000, 4500)))


def test_multimodal_call_uses_image_part_and_validates_result():
    client = MagicMock()
    client.models.generate_content.return_value = fake_api_response()
    result = analyze_screenshot(make_image(), language="हिन्दी (Hindi)", client=client, model_name="fake-test-model")
    assert result.risk_level == RiskLevel.CRITICAL
    assert result.explanation_language == "Hindi"
    client.models.generate_content.assert_called_once()
    kwargs = client.models.generate_content.call_args.kwargs
    assert kwargs["model"] == "fake-test-model"
    assert len(kwargs["contents"]) == 2
    assert kwargs["contents"][1].inline_data.mime_type == "image/jpeg"
    assert len(kwargs["contents"][1].inline_data.data) > 0
    assert "SCREENSHOT" in kwargs["contents"][0].text


def test_no_api_call_for_bad_image():
    client = MagicMock()
    with pytest.raises(InvalidInputError):
        analyze_screenshot(b"corrupt", client=client)
    client.models.generate_content.assert_not_called()


def test_quota_error_not_retried():
    client = MagicMock()
    client.models.generate_content.side_effect = APIError(429, {"error": {"code": 429, "message": "Quota exhausted"}})
    with pytest.raises(QuotaExceededError):
        analyze_screenshot(make_image(), client=client)
    client.models.generate_content.assert_called_once()


def test_service_error_not_retried():
    client = MagicMock()
    client.models.generate_content.side_effect = APIError(503, {"error": {"code": 503, "message": "Unavailable"}})
    with pytest.raises(ServiceUnavailableError):
        analyze_screenshot(make_image(), client=client)
    client.models.generate_content.assert_called_once()


def test_invalid_model_json_rejected_without_displaying_raw_json():
    client = MagicMock()
    response = MagicMock()
    response.text = "not valid json"
    client.models.generate_content.return_value = response
    with pytest.raises(FraudAnalysisError, match="invalid structured result"):
        analyze_screenshot(make_image(), client=client)


def test_schema_fields_pass_through_to_existing_result_type():
    client = MagicMock()
    client.models.generate_content.return_value = fake_api_response()
    result = analyze_screenshot(make_image(), client=client)
    assert result.scam_category == "Bank/KYC Impersonation"
    assert result.deceptive_tactics == ["OTP request"]
