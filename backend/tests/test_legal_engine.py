"""
Unit Tests for Legal Analysis Engine.
Tests document analysis, risk scoring, BNS/IPC mappings, and trilingual support.
"""

from app.services.legal_engine import LegalEngine

SAMPLE_TENANCY_DOC = """
RENTAL AGREEMENT
This agreement is entered between Owner (Lessor) and Tenant (Lessee).
1. Monthly rent is INR 25,000.
2. Tenant must deposit an advance of INR 1,00,000 which shall be non-refundable.
3. The Owner reserves the right to terminate this agreement immediately without any prior notice.
4. Tenant must pay a penalty of INR 5,000 per day in case of dispute.
5. In case of legal action, exclusive jurisdiction of the courts in Singapore shall apply.
"""

def test_document_analysis_detection_and_risk():
    res = LegalEngine.analyze_document(SAMPLE_TENANCY_DOC, language="en")
    assert "Rental" in res.document_type or "Agreement" in res.document_type
    assert res.risk_score >= 70  # Should be flagged high risk due to non-refundable deposit and unilateral termination
    assert len(res.clause_risks) >= 2
    assert len(res.action_plan) >= 2
    assert any("Tenancy" in law for law in res.governing_laws)

def test_trilingual_analysis():
    # Test Gujarati output
    res_gu = LegalEngine.analyze_document(SAMPLE_TENANCY_DOC, language="gu")
    assert "જોખમ સ્તર" in res_gu.summary
    assert res_gu.language == "gu"

    # Test Hindi output
    res_hi = LegalEngine.analyze_document(SAMPLE_TENANCY_DOC, language="hi")
    assert "जोखिम स्तर" in res_hi.summary
    assert res_hi.language == "hi"

def test_legal_chat_advisor_deposit():
    res = LegalEngine.legal_chat_advisor("My landlord refused to refund my deposit after I vacated the flat.", language="en")
    assert "Model Tenancy Act" in res.applicable_sections[0] or "Contract Act" in str(res.applicable_sections)
    assert len(res.next_steps) > 0

def test_legal_chat_advisor_cyber_fraud():
    res = LegalEngine.legal_chat_advisor("Someone stole 50000 rupees through OTP phishing fraud.", language="en")
    assert any("1930" in step or "1930" in res.answer for step in res.next_steps) or "1930" in res.answer
    assert any("Information Technology Act" in sec for sec in res.applicable_sections)

def test_bns_mapping_integrity():
    assert "318(4)" in LegalEngine.BNS_MAPPINGS["420"]["new_section"]
    assert "103" in LegalEngine.BNS_MAPPINGS["302"]["new_section"]
