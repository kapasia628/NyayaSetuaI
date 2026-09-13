"""
Unit Tests for Legal Aid Service and Section 12 Eligibility.
"""

from app.services.legal_aid_service import LegalAidService

def test_search_clinics_all():
    res = LegalAidService.search_clinics()
    assert res.total_found > 0
    assert "15100" in res.helpline_national

def test_search_clinics_by_state_and_district():
    res = LegalAidService.search_clinics(state="Gujarat", district="Surat")
    assert res.total_found == 1
    assert "Surat" in res.clinics[0].name

def test_eligibility_grounds():
    # Test SC/ST
    res1 = LegalAidService.check_eligibility(is_sc_or_st=True)
    assert res1["eligible_for_free_legal_aid"] is True

    # Test Workman
    res2 = LegalAidService.check_eligibility(is_industrial_workman=True)
    assert res2["eligible_for_free_legal_aid"] is True

    # Test Disabled
    res3 = LegalAidService.check_eligibility(is_disabled=True)
    assert res3["eligible_for_free_legal_aid"] is True

    # Test Custody
    res4 = LegalAidService.check_eligibility(is_in_custody=True)
    assert res4["eligible_for_free_legal_aid"] is True

    # Test High Income (Ineligible for free, but advice available)
    res5 = LegalAidService.check_eligibility(annual_income_inr=1000000)
    assert res5["eligible_for_free_legal_aid"] is False
