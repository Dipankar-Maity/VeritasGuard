"""
VeritasGuard - Pydantic v2 Data Schema for Cyber Fraud Analysis
Course: NVIDIA AI & Deep Learning Open Elective, Dayananda Sagar University
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class RiskLevel(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    CRITICAL = "Critical"
    UNCERTAIN = "Uncertain"


class FraudAnalysisResult(BaseModel):
    """
    Structured fraud analysis output produced by Gemini and validated via Pydantic v2.
    """
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    risk_level: RiskLevel = Field(
        ...,
        description="Assessed risk level: 'Low', 'Moderate', 'Critical', or 'Uncertain'."
    )
    scam_category: str = Field(
        ...,
        description="Identified fraud or scam category (e.g., Bank/KYC Impersonation, Lottery/Reward Scam, Job Scam, Electricity Bill Disconnection, Fake Delivery, Investment Fraud, None/Benign, etc.)."
    )
    deceptive_tactics: List[str] = Field(
        default_factory=list,
        description="List of specific deceptive tactics found (e.g., fake urgency, spoofed link, impersonation, threat of penalty, unverified APK download)."
    )
    psychological_manipulation: List[str] = Field(
        default_factory=list,
        description="Psychological triggers exploited (e.g., Fear of loss, Greed, Panic, False authority, Urgency, Curiosity)."
    )
    plain_language_explanation: str = Field(
        ...,
        description="Plain-language assessment in English, Hindi or Hinglish. Distinguish observations and inferences."
    )
    protective_actions: List[str] = Field(
        default_factory=list,
        description="Actionable, step-by-step protective recommendations for the user to stay safe."
    )
    urgency_level: Optional[str] = Field(
        default="Medium",
        description="Perceived urgency in the message: High, Medium, Low, or None."
    )
    explanation_language: str = Field(
        default="English",
        description="Language of the explanation: English, Hindi or Hinglish."
    )
    safety_disclaimer: str = Field(
        default="Automated AI Advisory: VeritasGuard analysis cannot guarantee 100% safety. Always exercise independent caution with unverified messages.",
        description="Mandatory disclaimer stating that no message can be guaranteed 100% safe."
    )
    observed_evidence: Optional[List[str]] = Field(
        default=None,
        description="Specific evidence observed in the message that supports the risk assessment."
    )
    unverified_assumptions: Optional[List[str]] = Field(
        default=None,
        description="Assumptions made during analysis that could not be independently verified."
    )
    uncertainty_explanation: Optional[str] = Field(
        default=None,
        description="Explanation of any uncertainty or ambiguity in the analysis result."
    )
    model_provider: Optional[str] = Field(
        default=None,
        description="Identifier for the AI model provider used (e.g., 'gemini', 'groq', 'gemini-langchain')."
    )

    def get_badge_color(self) -> str:
        """Return hex color corresponding to risk level for UI rendering."""
        colors = {
            RiskLevel.CRITICAL: "#ef4444",   # Red
            RiskLevel.MODERATE: "#f59e0b",   # Amber / Orange
            RiskLevel.LOW: "#10b981",        # Emerald Green
            RiskLevel.UNCERTAIN: "#6b7280",  # Gray
        }
        return colors.get(self.risk_level, "#6b7280")

    def get_badge_icon(self) -> str:
        """Return emoji icon corresponding to risk level."""
        icons = {
            RiskLevel.CRITICAL: "🚨",
            RiskLevel.MODERATE: "⚠️",
            RiskLevel.LOW: "🛡️",
            RiskLevel.UNCERTAIN: "❓",
        }
        return icons.get(self.risk_level, "❓")

