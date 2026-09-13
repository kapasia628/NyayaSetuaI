"""
Unit Tests for Advanced Legal Services:
- Statutory Limitation & Deadline Calculator (Limitation Act 1963)
- Bharatiya Nyaya Sanhita (BNS 2023) vs IPC 1860 Converter
"""

from app.models.schemas import LimitationCalculationRequest
from app.services.advanced_legal_service import LimitationCalculator, BNSConverter

def test_limitation_calculator_cheque_bounce():
    req = LimitationCalculationRequest(
        case_type="cheque_bounce_138",
        incident_date="2026-09-01",
        language="en"
    )
    res = LimitationCalculator.calculate(req)
    assert "Negotiable Instruments Act" in res.statute_name
    assert len(res.stages) == 3
    assert res.stages[0].stage_name == "Statutory Demand Notice to Drawer"
    assert res.condonation_of_delay_available is True

def test_limitation_calculator_consumer_complaint():
    req = LimitationCalculationRequest(
        case_type="consumer_complaint",
        incident_date="2025-01-01",
        language="en"
    )
    res = LimitationCalculator.calculate(req)
    assert "Consumer Protection Act" in res.statute_name
    assert len(res.stages) == 1
    assert "E-Daakhil" in res.stages[0].stage_name

def test_limitation_calculator_wages():
    req = LimitationCalculationRequest(
        case_type="unpaid_wages",
        incident_date="2024-05-10",
        language="en"
    )
    res = LimitationCalculator.calculate(req)
    assert "Limitation Act" in res.statute_name
    assert len(res.stages) >= 1

def test_bns_converter_cheating_420():
    res = BNSConverter.search("420")
    assert res.count >= 1
    assert "318(4)" in res.matches[0].new_bns_section
    assert "Cheating" in res.matches[0].offense_name

def test_bns_converter_murder_302():
    res = BNSConverter.search("murder")
    assert res.count >= 1
    assert "103" in res.matches[0].new_bns_section
    assert "Mob Lynching" in res.matches[0].offense_name

def test_bns_converter_theft_community_service():
    res = BNSConverter.search("theft")
    assert res.count >= 1
    assert "Community Service" in res.matches[0].punishment_summary

def test_bns_converter_general_fallback():
    res = BNSConverter.search("random_unknown_term_xyz")
    assert res.count >= 1
