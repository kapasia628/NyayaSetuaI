"""
Unit Tests for PII Redaction Module.
Verifies Indian identification numbers, phones, emails, and bank accounts are sanitized.
"""

from app.core.security import PIIRedactor

def test_aadhaar_redaction():
    text = "My Aadhaar card number is 3456 7890 1234 and my brother's is 987654321098."
    redacted, items = PIIRedactor.redact(text)
    assert "3456 7890 1234" not in redacted
    assert "987654321098" not in redacted
    assert "[REDACTED_AADHAAR_" in redacted
    assert len(items) == 2

def test_pan_redaction():
    text = "The assessee's PAN card is ABCDE1234F registered with the Income Tax Department."
    redacted, items = PIIRedactor.redact(text)
    assert "ABCDE1234F" not in redacted
    assert "[REDACTED_PAN_ABXXXXXF]" in redacted
    assert len(items) == 1

def test_phone_and_email_redaction():
    text = "Reach out to me at +91 9876543210 or via email lawyer.help@example.gov.in immediately."
    redacted, items = PIIRedactor.redact(text)
    assert "9876543210" not in redacted
    assert "lawyer.help@example.gov.in" not in redacted
    assert "[REDACTED_PHONE_" in redacted
    assert "[REDACTED_EMAIL_" in redacted

def test_bank_account_redaction():
    text = "Kindly refund the deposit into Account No: 12345678901234."
    redacted, items = PIIRedactor.redact(text)
    assert "12345678901234" not in redacted
    assert "[REDACTED_BANK_ACCOUNT_" in redacted

def test_empty_string():
    redacted, items = PIIRedactor.redact("")
    assert redacted == ""
    assert items == []
