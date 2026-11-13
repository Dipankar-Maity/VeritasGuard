"""
VeritasGuard - Cyber Fraud Taxonomy Module
Course: NVIDIA AI & Deep Learning Open Elective, Dayananda Sagar University

Provides a PROJECT-DEFINED educational taxonomy inspired by common fraud patterns.
Labels here are not an official government classification scheme.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TaxonomyCategory:
    """Represents a single cyber fraud / scam category in the VeritasGuard taxonomy."""
    id: str
    display_name: str
    description: str
    official_reference: str
    keywords: List[str] = field(default_factory=list)


TAXONOMY: List[TaxonomyCategory] = [
    TaxonomyCategory(
        id="banking_kyc_impersonation",
        display_name="Banking and KYC Impersonation",
        description=(
            "Fraudsters impersonate bank officials, RBI, or SEBI to trick victims into "
            "sharing net banking credentials, OTPs, Aadhaar/PAN details, or visiting "
            "phishing websites for fake KYC updates."
        ),
        official_reference="Project-defined educational category; report suspected cybercrime at cybercrime.gov.in",
        keywords=[
            "kyc", "account blocked", "net banking", "otp", "aadhaar", "pan card",
            "sbi", "hdfc", "icici", "axis bank", "rbi", "sebi", "bank", "credit card",
            "debit card", "atm pin", "ifsc", "phishing", "account suspension",
        ],
    ),
    TaxonomyCategory(
        id="upi_payment_fraud",
        display_name="UPI and Payment Fraud",
        description=(
            "Scams involving UPI payment requests, fake collect requests, reverse UPI "
            "trick (victim pays instead of receiving), or impersonation of payment apps "
            "like PhonePe, GPay, Paytm, or BHIM."
        ),
        official_reference="Project-defined educational category; report suspected cybercrime at cybercrime.gov.in",
        keywords=[
            "upi", "phonepe", "gpay", "google pay", "paytm", "bhim", "neft", "imps",
            "collect request", "scan qr", "payment link", "transfer money", "refund",
            "cashback", "upi pin", "receive money",
        ],
    ),
    TaxonomyCategory(
        id="electricity_bill_scam",
        display_name="Electricity Bill Disconnection Scam",
        description=(
            "Fraudsters impersonate electricity board employees, threatening immediate "
            "power disconnection if the victim does not call a fake helpline number and "
            "pay or install a remote-access APK."
        ),
        official_reference="Project-defined educational category; report suspected cybercrime at cybercrime.gov.in",
        keywords=[
            "electricity", "power cut", "disconnection", "bescom", "tata power",
            "bses", "msedcl", "electricity officer", "bill pending", "meter",
            "consumer number", "bijli", "current bill", "power supply",
        ],
    ),
    TaxonomyCategory(
        id="fake_delivery_scam",
        display_name="Fake Delivery or Courier Scam",
        description=(
            "Scammers impersonate courier services (FedEx, BlueDart, India Post, Delhivery) "
            "or customs officials to demand custom duty fees, OTPs, or remote access to "
            "release a 'parcel' that does not exist."
        ),
        official_reference="Project-defined educational category; report suspected cybercrime at cybercrime.gov.in",
        keywords=[
            "parcel", "courier", "fedex", "bluedart", "india post", "delhivery",
            "customs duty", "package", "shipment", "delivery", "customs officer",
            "narcotics", "seized", "tracking", "out for delivery",
        ],
    ),
    TaxonomyCategory(
        id="fake_job_task_scam",
        display_name="Fake Job or Task-Based Scam",
        description=(
            "Victims are lured with unrealistic work-from-home job offers (liking YouTube "
            "videos, reviewing hotels, crypto trading tasks) that initially pay small amounts "
            "then demand large 'prepaid task' deposits that are never returned."
        ),
        official_reference="Project-defined educational category; report suspected cybercrime at cybercrime.gov.in",
        keywords=[
            "work from home", "part time", "earn daily", "youtube like", "telegram",
            "vip channel", "task", "review", "rating", "recruitment", "hr",
            "job offer", "salary", "per day earn", "upi payout", "easy money",
        ],
    ),
    TaxonomyCategory(
        id="lottery_reward_scam",
        display_name="Lottery and Reward Scam",
        description=(
            "Fraudulent notifications claiming the victim has won a lottery, lucky draw, "
            "KBC (Kaun Banega Crorepati) prize, or government reward, requiring upfront "
            "processing fees or tax payments before release of non-existent winnings."
        ),
        official_reference="Project-defined educational category; report suspected cybercrime at cybercrime.gov.in",
        keywords=[
            "lottery", "winner", "prize", "kbc", "lucky draw", "congratulations",
            "reward", "won", "cash prize", "claim your prize", "processing fee",
            "tax payment", "jackpot", "bumper prize", "amazon lucky winner",
        ],
    ),
    TaxonomyCategory(
        id="fake_govt_authority",
        display_name="Fake Government Authority Impersonation",
        description=(
            "Scammers impersonate police officers, CBI/ED agents, TRAI, Income Tax, "
            "Narcotics Bureau, or government officials to threaten arrest, court summons, "
            "or account freezing unless an immediate bribe or fine is paid."
        ),
        official_reference="Project-defined educational category; report suspected cybercrime at cybercrime.gov.in",
        keywords=[
            "cbi", "police", "enforcement directorate", "ed", "trai", "income tax",
            "narcotics", "arrest warrant", "court notice", "legal action", "fir",
            "government", "notice", "penalty", "fine", "customs", "visa",
        ],
    ),
    TaxonomyCategory(
        id="investment_crypto_fraud",
        display_name="Investment and Cryptocurrency Fraud",
        description=(
            "Victims are enticed with guaranteed high-return investment schemes, fake "
            "stock trading apps, crypto trading bots, or Ponzi/MLM schemes that result "
            "in total loss of invested capital."
        ),
        official_reference="Project-defined educational category; report suspected cybercrime at cybercrime.gov.in",
        keywords=[
            "investment", "returns", "profit", "crypto", "bitcoin", "trading",
            "stock market", "mutual fund", "demat", "sebi registered", "ponzi",
            "mlm", "doubling money", "guaranteed returns", "nse", "bse", "share tips",
        ],
    ),
    TaxonomyCategory(
        id="malicious_apk_remote",
        display_name="Malicious APK or Remote Access Request",
        description=(
            "Fraudsters trick victims into installing malicious Android APKs or legitimate "
            "remote-access tools (AnyDesk, TeamViewer, QuickSupport) to gain full device "
            "control, enabling unauthorized banking transactions."
        ),
        official_reference="Project-defined educational category; report suspected cybercrime at cybercrime.gov.in",
        keywords=[
            "apk", "anydesk", "teamviewer", "quicksupport", "install app", "download",
            "screen share", "remote access", "support app", "customer care",
            "verify otp", "grant permission", "accessibility", "sideload",
        ],
    ),
    TaxonomyCategory(
        id="qr_payment_scam",
        display_name="QR Payment Scam",
        description=(
            "Scammers send QR codes or UPI links under pretexts like 'scan to receive money', "
            "product refunds, or online marketplace deals, tricking victims into authorizing "
            "payment instead of receiving it."
        ),
        official_reference="Project-defined educational category; report suspected cybercrime at cybercrime.gov.in",
        keywords=[
            "qr code", "scan", "receive money", "qr", "payment qr", "upi qr",
            "scan to get refund", "olx", "quikr", "marketplace", "scan and pay",
        ],
    ),
    TaxonomyCategory(
        id="possible_legitimate",
        display_name="Possible Legitimate Communication",
        description=(
            "Message appears to follow legitimate communication patterns from known entities "
            "(e.g., official OTP from a recognized bank header, delivery notifications from "
            "known services), though automated analysis cannot guarantee authenticity."
        ),
        official_reference="Project-defined",
        keywords=[
            "otp", "transaction alert", "official", "registered", "authorized",
            "do not share", "bank statement", "account credit", "debit alert",
        ],
    ),
    TaxonomyCategory(
        id="unknown_insufficient",
        display_name="Unknown or Insufficient Evidence",
        description=(
            "The message does not contain enough context, detail, or recognizable fraud "
            "indicators to classify it reliably into any known scam category. Human review "
            "is recommended."
        ),
        official_reference="Project-defined",
        keywords=[],
    ),
]


def list_all_categories() -> List[TaxonomyCategory]:
    """Return the full list of all VeritasGuard taxonomy categories."""
    return TAXONOMY


def get_category_by_name(name: str) -> Optional[TaxonomyCategory]:
    """
    Look up a taxonomy category by id or display_name using case-insensitive partial matching.

    Args:
        name: Partial or full name to search for (matched against id and display_name).

    Returns:
        The first matching TaxonomyCategory, or None if not found.
    """
    name_lower = name.lower().strip()
    for category in TAXONOMY:
        if name_lower in category.id.lower() or name_lower in category.display_name.lower():
            return category
    return None
