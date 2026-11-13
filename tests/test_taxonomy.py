"""Taxonomy labels are project-defined; no official endorsement claimed."""
from taxonomy import list_all_categories, get_category_by_name


def test_taxonomy_contains_required_scenarios():
    names = " ".join(c.display_name.lower() for c in list_all_categories())
    assert "qr" in names
    assert "kyc" in names
    assert "electricity" in names
    assert "courier" in names or "delivery" in names
    assert len(list_all_categories()) >= 10


def test_lookup_known_category():
    assert get_category_by_name("banking_kyc_impersonation") is not None
