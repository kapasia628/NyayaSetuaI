"""
Security and Data Privacy Module for NyayaSetu AI.
Implements automated Indian PII (Personally Identifiable Information) Redaction,
Prompt Injection defense, and Input Sanitization for legal confidentiality.
"""

import re
from typing import Dict, List, Tuple

class PIIRedactor:
    """
    Detects and masks sensitive personal identifiable information (PII)
    specific to Indian citizens and global standards before text is processed.
    """
    
    # Regex patterns for sensitive identifiers
    PATTERNS: Dict[str, re.Pattern] = {
        # Indian Aadhaar: 12 digits (often grouped as 4 4 4 or continuous)
        "AADHAAR": re.compile(r"\b[2-9]{1}[0-9]{3}\s?[0-9]{4}\s?[0-9]{4}\b"),
        
        # Indian PAN Card: 5 uppercase letters, 4 digits, 1 uppercase letter
        "PAN": re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b"),
        
        # Indian Mobile Numbers (+91 or starting with 6,7,8,9)
        "PHONE": re.compile(r"(?:\+91[\s\-]?)?[6-9]\d{9}\b"),
        
        # Email Addresses
        "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"),
        
        # Bank Account Numbers: 9 to 18 digits (with word context or standalone long sequence)
        "BANK_ACCOUNT": re.compile(r"\b(?:A/C|Account|Acc)(?:\s*No\.?|\s*Number)?\s*[:#-]?\s*([0-9]{9,18})\b", re.IGNORECASE),
        
        # Indian Passport Number: 1 uppercase letter + 7 digits
        "PASSPORT": re.compile(r"\b[A-PR-WYa-pr-wy][1-9]\d\s?\d{4}[1-9]\b"),
        
        # Indian Vehicle Registration (e.g. GJ-01-AB-1234 or DL01AB1234)
        "VEHICLE_NO": re.compile(r"\b[A-Z]{2}[-\s]?[0-9]{1,2}[-\s]?[A-Z]{1,3}[-\s]?[0-9]{4}\b"),
    }

    @classmethod
    def redact(cls, text: str) -> Tuple[str, List[Dict[str, str]]]:
        """
        Redacts detected PII from text, replacing it with tokenized placeholders.
        Returns the sanitized text and a list of redactions performed.
        """
        if not text:
            return "", []

        sanitized_text = text
        redactions: List[Dict[str, str]] = []

        # Mask Bank Accounts first (to avoid conflict with phone/aadhaar)
        def replace_bank(match):
            ac_num = match.group(1)
            masked = f"[REDACTED_BANK_ACCOUNT_{ac_num[-4:] if len(ac_num)>=4 else 'XXXX'}]"
            redactions.append({"type": "BANK_ACCOUNT", "masked": masked})
            return match.group(0).replace(ac_num, masked)

        sanitized_text = cls.PATTERNS["BANK_ACCOUNT"].sub(replace_bank, sanitized_text)

        # Mask Aadhaar
        def replace_aadhaar(match):
            aadhaar = match.group(0).replace(" ", "")
            masked = f"[REDACTED_AADHAAR_XXXX-XXXX-{aadhaar[-4:]}]"
            redactions.append({"type": "AADHAAR", "masked": masked})
            return masked

        sanitized_text = cls.PATTERNS["AADHAAR"].sub(replace_aadhaar, sanitized_text)

        # Mask PAN
        def replace_pan(match):
            pan = match.group(0)
            masked = f"[REDACTED_PAN_{pan[:2]}XXXXX{pan[-1]}]"
            redactions.append({"type": "PAN", "masked": masked})
            return masked

        sanitized_text = cls.PATTERNS["PAN"].sub(replace_pan, sanitized_text)

        # Mask Phone
        def replace_phone(match):
            phone = match.group(0)
            clean = re.sub(r"\D", "", phone)
            masked = f"[REDACTED_PHONE_XXXXX{clean[-4:] if len(clean)>=4 else 'XXXX'}]"
            redactions.append({"type": "PHONE", "masked": masked})
            return masked

        sanitized_text = cls.PATTERNS["PHONE"].sub(replace_phone, sanitized_text)

        # Mask Email
        def replace_email(match):
            email = match.group(0)
            parts = email.split("@")
            masked = f"[REDACTED_EMAIL_{parts[0][:2]}***@{parts[1]}]"
            redactions.append({"type": "EMAIL", "masked": masked})
            return masked

        sanitized_text = cls.PATTERNS["EMAIL"].sub(replace_email, sanitized_text)

        # Mask Passport
        def replace_passport(match):
            masked = "[REDACTED_PASSPORT]"
            redactions.append({"type": "PASSPORT", "masked": masked})
            return masked

        sanitized_text = cls.PATTERNS["PASSPORT"].sub(replace_passport, sanitized_text)

        return sanitized_text, redactions


class SecurityGuard:
    """
    Sanitizes user inputs against Prompt Injections, Jailbreak payloads,
    and Malicious script injections.
    """
    
    PROMPT_INJECTION_PATTERNS = [
        re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions", re.IGNORECASE),
        re.compile(r"disregard\s+(all\s+)?(previous|prior)\s+rules", re.IGNORECASE),
        re.compile(r"you\s+are\s+now\s+in\s+DAN\s+mode", re.IGNORECASE),
        re.compile(r"reveal\s+(your\s+)?(system\s+prompt|secret\s+key|api\s+key)", re.IGNORECASE),
        re.compile(r"jailbreak", re.IGNORECASE),
        re.compile(r"<script.*?>.*?</script>", re.IGNORECASE | re.DOTALL),
        re.compile(r"javascript:\s*", re.IGNORECASE),
    ]

    @classmethod
    def check_input_safety(cls, text: str) -> Tuple[bool, str]:
        """
        Validates text for injection or exploit attempts.
        Returns (is_safe: bool, reason: str).
        """
        if not text:
            return True, "Safe"

        for pattern in cls.PROMPT_INJECTION_PATTERNS:
            if pattern.search(text):
                return False, "Security violation: Potential adversarial prompt injection or script detected."

        return True, "Safe"

    @classmethod
    def sanitize_html(cls, text: str) -> str:
        """Escapes dangerous HTML entities to prevent stored XSS."""
        if not text:
            return ""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")
        )
