"""
Unit tests for VeritasGuard Pydantic v2 Schema
Course: NVIDIA AI & Deep Learning Open Elective, Dayananda Sagar University
"""

import pytest
from pydantic import ValidationError
from schema import FraudAnalysisResult, RiskLevel


def test_valid_fraud_analysis_result():
    """Verify that a well-formed dictionary validates properly into FraudAnalysisResult."""
    data = {
        "risk_level": "Critical",
        "scam_category": "Electricity Bill Scam",
        "deceptive_tactics": ["Urgent threat of disconnection", "Fake phone number"],
        "psychological_manipulation": ["Fear", "Urgency"],
        "plain_language_explanation": "This message is a fraudulent threat to cut power and cause disconnection unless money is paid.",
        "protective_actions": ["Do not call", "Contact electricity board directly"],
        "urgency_level": "High",
        "explanation_language": "English",
    }
    result = FraudAnalysisResult(**data)
    assert result.risk_level == RiskLevel.CRITICAL
    assert result.scam_category == "Electricity Bill Scam"
    assert len(result.deceptive_tactics) == 2
    assert len(result.psychological_manipulation) == 2
    assert "disconnection" in result.plain_language_explanation
    assert len(result.protective_actions) == 2
    assert result.urgency_level == "High"
    assert "VeritasGuard" in result.safety_disclaimer or "safety" in result.safety_disclaimer.lower()


def test_all_risk_levels():
    """Ensure all valid RiskLevel enum values are accepted and mapped correctly."""
    valid_levels = ["Low", "Moderate", "Critical", "Uncertain"]
    for level in valid_levels:
        result = FraudAnalysisResult(
            risk_level=level,
            scam_category="Test",
            plain_language_explanation="Test explanation",
        )
        assert result.risk_level.value == level


def test_invalid_risk_level_raises_validation_error():
    """Ensure invalid risk levels trigger a Pydantic ValidationError."""
    with pytest.raises(ValidationError):
        FraudAnalysisResult(
            risk_level="SuperDangerous",  # Not a valid enum
            scam_category="Phishing",
            plain_language_explanation="Expl",
        )


def test_missing_required_fields_raises_error():
    """Verify missing required fields (like plain_language_explanation) raise ValidationError."""
    with pytest.raises(ValidationError):
        FraudAnalysisResult(
            risk_level="Critical",
            # Missing scam_category and plain_language_explanation
        )


def test_json_serialization_and_deserialization():
    """Verify round-trip JSON serialization with Pydantic v2 model_dump_json and model_validate_json."""
    original = FraudAnalysisResult(
        risk_level=RiskLevel.MODERATE,
        scam_category="Lottery Scam",
        deceptive_tactics=["Unsolicited prize", "Advance fee request"],
        psychological_manipulation=["Greed"],
        plain_language_explanation="User is promised winnings for an unentered contest.",
        protective_actions=["Ignore the message", "Never pay fees to claim prizes"],
        explanation_language="English",
    )
    json_str = original.model_dump_json()
    assert isinstance(json_str, str)

    restored = FraudAnalysisResult.model_validate_json(json_str)
    assert restored.risk_level == RiskLevel.MODERATE
    assert restored.scam_category == original.scam_category
    assert restored.deceptive_tactics == original.deceptive_tactics


def test_badge_color_and_icon_helpers():
    """Test UI helper methods for color badges and icons."""
    res_crit = FraudAnalysisResult(
        risk_level=RiskLevel.CRITICAL,
        scam_category="Scam",
        plain_language_explanation="Desc",
    )
    assert res_crit.get_badge_color() == "#ef4444"
    assert res_crit.get_badge_icon() == "🚨"

    res_low = FraudAnalysisResult(
        risk_level=RiskLevel.LOW,
        scam_category="Alert",
        plain_language_explanation="Desc",
    )
    assert res_low.get_badge_color() == "#10b981"
    assert res_low.get_badge_icon() == "🛡️"

    res_mod = FraudAnalysisResult(
        risk_level=RiskLevel.MODERATE,
        scam_category="Promo",
        plain_language_explanation="Desc",
    )
    assert res_mod.get_badge_color() == "#f59e0b"
    assert res_mod.get_badge_icon() == "⚠️"

    res_unc = FraudAnalysisResult(
        risk_level=RiskLevel.UNCERTAIN,
        scam_category="Unknown",
        plain_language_explanation="Desc",
    )
    assert res_unc.get_badge_color() == "#6b7280"
    assert res_unc.get_badge_icon() == "❓"


def test_extra_fields_ignored_gracefully():
    """Ensure any unforeseen extra fields returned by LLM are ignored without crashing."""
    raw_json = """{
        "risk_level": "Low",
        "scam_category": "Legitimate",
        "plain_language_explanation": "Safe looking notice.",
        "extra_unwanted_ai_field": "some commentary",
        "another_field": 12345
    }"""
    result = FraudAnalysisResult.model_validate_json(raw_json)
    assert result.risk_level == RiskLevel.LOW
    assert not hasattr(result, "extra_unwanted_ai_field")
