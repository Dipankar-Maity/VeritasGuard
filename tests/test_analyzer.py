"""
Unit and integration tests for VeritasGuard Analyzer Engine
Course: NVIDIA AI & Deep Learning Open Elective, Dayananda Sagar University
"""

import pytest
from unittest.mock import MagicMock, patch
from google.genai.errors import APIError

from schema import FraudAnalysisResult, RiskLevel
from analyzer import (
    analyze_message,
    get_offline_demo_samples,
    get_configured_model,
    get_genai_client,
    InvalidInputError,
    ConfigurationError,
    QuotaExceededError,
    ServiceUnavailableError,
    NetworkError,
    FraudAnalysisError,
)


def test_empty_input_raises_invalid_input_error():
    """Verify that empty or whitespace-only messages raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        analyze_message("")

    with pytest.raises(InvalidInputError):
        analyze_message("   \n\t  ")


def test_missing_api_key_raises_configuration_error(monkeypatch):
    """Verify that missing GEMINI_API_KEY raises ConfigurationError."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(ConfigurationError):
        get_genai_client(api_key=None)


def test_get_configured_model_default(monkeypatch):
    """Verify default model fallback is gemini-3.8-flash."""
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    assert get_configured_model() == "gemini-3.8-flash"


def test_offline_demo_samples_integrity():
    """Ensure predefined synthetic demo samples are well-formed and valid."""
    samples = get_offline_demo_samples()
    assert len(samples) >= 4, "Expected at least 4 predefined synthetic samples"

    categories = set()
    languages = set()
    risk_levels = set()

    for sample in samples:
        assert "id" in sample
        assert "title" in sample
        assert "type" in sample
        assert "message" in sample
        assert len(sample["message"]) > 10
        assert "result" in sample
        assert isinstance(sample["result"], FraudAnalysisResult)
        assert sample["result"].plain_language_explanation
        assert len(sample["result"].protective_actions) > 0

        categories.add(sample["result"].scam_category)
        languages.add(sample["result"].explanation_language)
        risk_levels.add(sample["result"].risk_level)

    # Check language and risk level diversity
    assert "English" in languages
    assert "Hindi" in languages
    assert RiskLevel.CRITICAL in risk_levels
    assert RiskLevel.LOW in risk_levels


def test_analyzer_handles_mocked_successful_response():
    """Verify analyzer correctly parses a successful JSON response from a mock client."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = """{
        "risk_level": "Critical",
        "scam_category": "Bank Impersonation",
        "deceptive_tactics": ["Fake link", "Immediate suspension threat"],
        "psychological_manipulation": ["Panic", "Urgency"],
        "plain_language_explanation": "The message attempts to steal login credentials.",
        "protective_actions": ["Do not click link", "Call bank helpline 1930"],
        "urgency_level": "High",
        "explanation_language": "English",
        "safety_disclaimer": "VeritasGuard disclaimer"
    }"""
    mock_client.models.generate_content.return_value = mock_response

    result = analyze_message(
        message_text="Your bank account is blocked. Visit http://fake-bank.com",
        client=mock_client,
    )

    assert result.risk_level == RiskLevel.CRITICAL
    assert result.scam_category == "Bank Impersonation"
    assert len(result.deceptive_tactics) == 2
    assert "1930" in result.protective_actions[1]


def test_analyzer_handles_markdown_wrapped_json():
    """Verify analyzer strips markdown ```json ``` code fences before parsing."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = """```json
    {
        "risk_level": "Moderate",
        "scam_category": "Work From Home Scam",
        "deceptive_tactics": ["Unrealistic salary"],
        "psychological_manipulation": ["Greed"],
        "plain_language_explanation": "Part-time job requiring upfront deposit.",
        "protective_actions": ["Block sender"],
        "explanation_language": "English"
    }
    ```"""
    mock_client.models.generate_content.return_value = mock_response

    result = analyze_message(
        message_text="Earn 10000 daily by liking videos",
        client=mock_client,
    )

    assert result.risk_level == RiskLevel.MODERATE
    assert result.scam_category == "Work From Home Scam"


def test_analyzer_handles_quota_exceeded_error():
    """Verify that HTTP 429 / RESOURCE_EXHAUSTED raises QuotaExceededError."""
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = APIError(
        429,
        {"error": {"code": 429, "message": "RESOURCE_EXHAUSTED: Quota exceeded."}}
    )

    with pytest.raises(QuotaExceededError):
        analyze_message(
            message_text="Suspicious message",
            client=mock_client,
        )


def test_analyzer_handles_service_unavailable_error():
    """Verify that HTTP 503 / UNAVAILABLE raises ServiceUnavailableError."""
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = APIError(
        503,
        {"error": {"code": 503, "message": "UNAVAILABLE: Model is experiencing high demand."}}
    )

    with pytest.raises(ServiceUnavailableError):
        analyze_message(
            message_text="Suspicious message",
            client=mock_client,
        )


def test_analyzer_handles_network_timeout():
    """Verify that connection/network timeouts raise NetworkError."""
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = TimeoutError("Connection timed out")

    with pytest.raises(NetworkError):
        analyze_message(
            message_text="Suspicious message",
            client=mock_client,
        )


def test_analyzer_handles_invalid_json_response():
    """Verify that garbled or malformed JSON from model raises FraudAnalysisError."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "This is not JSON at all! Just some text."
    mock_client.models.generate_content.return_value = mock_response

    with pytest.raises(FraudAnalysisError):
        analyze_message(
            message_text="Suspicious message",
            client=mock_client,
        )
