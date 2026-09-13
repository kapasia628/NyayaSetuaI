"""
Unit Tests for Drafting Engine.
Validates legal notice templates, RTI drafts, and consumer grievances.
"""

from app.models.schemas import LegalDraftRequest
from app.services.drafting_engine import DraftingEngine

def test_draft_salary_notice():
    req = LegalDraftRequest(
        template_type="unpaid_salary_notice",
        sender_name="Ramesh Patel",
        sender_address="102, Shivalik Hills, Ahmedabad, Gujarat",
        recipient_name="Tech Solutions Pvt Ltd",
        recipient_address="Plot 44, Infocity, Gandhinagar, Gujarat",
        details={
            "amount_owed": "1,50,000",
            "work_duration": "Jan 2024 to Aug 2024",
            "designation": "Senior Web Developer"
        },
        language="en"
    )
    draft = DraftingEngine.generate_draft(req)
    assert "Payment of Wages Act" in draft.draft_body
    assert "1,50,000" in draft.draft_body
    assert "Ramesh Patel" in draft.draft_body
    assert draft.statutory_notice_period_days == 15

def test_draft_rent_deposit_notice():
    req = LegalDraftRequest(
        template_type="rent_deposit_notice",
        sender_name="Pooja Sharma",
        sender_address="Flat 304, Green Acres, Surat",
        recipient_name="Mr. Suresh Mehta",
        recipient_address="Bungalow 12, VIP Road, Surat",
        details={
            "deposit_amount": "60,000",
            "vacated_date": "August 31, 2024",
            "property_address": "Flat 304, Green Acres, Surat"
        },
        language="en"
    )
    draft = DraftingEngine.generate_draft(req)
    assert "SECURITY DEPOSIT" in draft.subject
    assert "60,000" in draft.draft_body
    assert draft.statutory_notice_period_days == 15

def test_draft_rti_application():
    req = LegalDraftRequest(
        template_type="rti_application",
        sender_name="Mohanlal Joshi",
        sender_address="Ward 5, Rajkot, Gujarat",
        recipient_name="Public Information Officer",
        recipient_address="Municipal Corporation Office, Rajkot",
        details={
            "department_name": "Roads and Infrastructure Department",
            "queries": [
                "Status of pothole repair work tender on Ring Road.",
                "Funds sanctioned and name of contractor."
            ]
        },
        language="en"
    )
    draft = DraftingEngine.generate_draft(req)
    assert "SECTION 6(1)" in draft.subject
    assert "30 (thirty) days" in draft.draft_body
    assert draft.statutory_notice_period_days == 30

def test_draft_consumer_notice():
    req = LegalDraftRequest(
        template_type="consumer_complaint",
        sender_name="Vikram Singh",
        sender_address="Chandigarh",
        recipient_name="Mega Electronics",
        recipient_address="Delhi",
        details={
            "product_service_name": "Smart Television",
            "amount_paid": "45,000",
            "defect_description": "Motherboard malfunction within 2 weeks"
        },
        language="en"
    )
    draft = DraftingEngine.generate_draft(req)
    assert "CONSUMER PROTECTION ACT" in draft.subject
    assert "45,000" in draft.draft_body
    assert "Smart Television" in draft.draft_body

def test_draft_cease_and_desist():
    req = LegalDraftRequest(
        template_type="cease_and_desist",
        sender_name="Anjali Sharma",
        sender_address="Jaipur",
        recipient_name="XYZ Defamation Agency",
        recipient_address="Noida",
        details={
            "unlawful_act": "Publishing false defamatory statements on social media"
        },
        language="en"
    )
    draft = DraftingEngine.generate_draft(req)
    assert "CEASE AND DESIST" in draft.subject
    assert "356" in str(draft.legal_references)
    assert draft.statutory_notice_period_days == 7

def test_draft_general_notice():
    req = LegalDraftRequest(
        template_type="custom_type",
        sender_name="Sunil Rao",
        sender_address="Hyderabad",
        recipient_name="Tenant",
        recipient_address="Flat 10",
        details={},
        language="en"
    )
    draft = DraftingEngine.generate_draft(req)
    assert "STATUTORY LEGAL NOTICE" in draft.subject

