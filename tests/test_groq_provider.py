"""Optional Groq provider and explicit text-only fallback, fully mocked."""
from unittest.mock import MagicMock, patch
import pytest
from analyzer import (analyze_message_groq, analyze_text_with_provider,
                      get_groq_client, ConfigurationError, ServiceUnavailableError)
from schema import RiskLevel


def mock_config():
    cfg = {"client": MagicMock(), "model": "openai/gpt-oss-120b"}
    fake = MagicMock()
    fake.choices[0].message.content = '{"risk_level":"Moderate", "scam_category":"Job lure", "plain_language_explanation":"Suspicious offer"}'
    cfg["client"].chat.completions.create.return_value = fake
    return cfg


def test_groq_requires_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(ConfigurationError):
        get_groq_client()


def test_mock_groq_analysis_validates_json():
    cfg = mock_config()
    result = analyze_message_groq("Join Telegram work group", groq_config=cfg)
    assert result.risk_level == RiskLevel.MODERATE
    assert result.model_provider == "groq"
    assert cfg["client"].chat.completions.create.call_count == 1
    kwargs = cfg["client"].chat.completions.create.call_args.kwargs
    assert kwargs["response_format"]["type"] == "json_schema"
    fmt = kwargs["response_format"]["json_schema"]
    assert fmt["strict"] is True
    assert fmt["schema"]["additionalProperties"] is False
    assert set(fmt["schema"]["required"]) == set(fmt["schema"]["properties"])


def test_explicit_provider_opt_in_only():
    with patch("analyzer.analyze_message", side_effect=ServiceUnavailableError("off")) as gemini,          patch("analyzer.analyze_message_groq") as groq:
        with pytest.raises(ServiceUnavailableError):
            analyze_text_with_provider("urgent", fallback_to_groq=False)
        groq.assert_not_called()
        analyze_text_with_provider("urgent", fallback_to_groq=True)
        groq.assert_called_once()
        assert gemini.call_count == 2


def test_invalid_json_hidden():
    cfg = mock_config()
    cfg["client"].chat.completions.create.return_value.choices[0].message.content = 'invalid JSON with private details'
    from analyzer import FraudAnalysisError
    with pytest.raises(FraudAnalysisError) as exc:
        analyze_message_groq("Fraud test", groq_config=cfg)
    assert "private" not in str(exc.value)


def test_groq_schema_enforces_real_fields():
    from analyzer import _groq_response_format
    fmt = _groq_response_format("openai/gpt-oss-120b")
    schema = fmt["json_schema"]["schema"]
    assert set(["risk_level", "scam_category", "plain_language_explanation",
                "protective_actions", "deceptive_tactics",
                "psychological_manipulation"]).issubset(schema["required"])
    assert schema["properties"]["risk_level"]["enum"] == [
        "Low", "Moderate", "Critical", "Uncertain"
    ]


def test_groq_other_model_uses_best_effort_schema_mode():
    from analyzer import _groq_response_format
    assert _groq_response_format("other-model")["json_schema"]["strict"] is False
