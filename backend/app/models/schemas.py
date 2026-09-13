"""
Pydantic Schemas for NyayaSetu AI API.
Strict type validation, comprehensive docstrings, and Swagger documentation support.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# ================= Document Simplification Schemas =================

class ClauseRisk(BaseModel):
    clause_title: str = Field(..., description="Title or identifier of the legal clause")
    original_excerpt: str = Field(..., description="Excerpt from the original document")
    risk_level: str = Field(..., description="Risk severity: HIGH, MEDIUM, LOW, or INFORMATIONAL")
    explanation: str = Field(..., description="Clear explanation in layman's language")
    recommended_action: str = Field(..., description="Suggested safeguard or citizen response")

class ActionItem(BaseModel):
    step: int = Field(..., description="Priority sequence order")
    action: str = Field(..., description="Action to be taken")
    deadline: Optional[str] = Field(None, description="Legal deadline or timeframe if applicable")
    authority: Optional[str] = Field(None, description="Relevant legal forum or authority")

class DocumentAnalysisRequest(BaseModel):
    document_text: str = Field(..., min_length=10, max_length=50000, description="Raw legal notice or contract text")
    language: str = Field("en", description="Target output language: 'en', 'hi', or 'gu'")
    redact_pii: bool = Field(True, description="Whether to automatically redact sensitive personal information")

class DocumentAnalysisResponse(BaseModel):
    document_type: str = Field(..., description="Categorized document type e.g. Legal Notice, Rental Agreement, FIR")
    summary: str = Field(..., description="Plain-language summary understandable by a common citizen")
    key_dates: List[str] = Field(default_factory=list, description="Critical dates, response windows, or milestones")
    governing_laws: List[str] = Field(default_factory=list, description="Applicable Indian laws and sections")
    risk_score: int = Field(..., ge=0, le=100, description="Overall citizen risk score (0 to 100)")
    clause_risks: List[ClauseRisk] = Field(default_factory=list, description="Identified clauses and their risk assessment")
    action_plan: List[ActionItem] = Field(default_factory=list, description="Step-by-step citizen action checklist")
    pii_redacted: bool = Field(..., description="Whether PII was redacted")
    redactions_count: int = Field(0, description="Number of sensitive PII tokens masked")
    language: str = Field("en", description="Response language")

# ================= Legal Chat Schemas =================

class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message text")

class LegalChatRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=2000, description="Citizen's legal question or situation")
    conversation_history: List[ChatMessage] = Field(default_factory=list, description="Previous messages in session")
    language: str = Field("en", description="Preferred response language: 'en', 'hi', or 'gu'")

class LegalChatResponse(BaseModel):
    answer: str = Field(..., description="Layman-friendly legal advice and guidance")
    applicable_sections: List[str] = Field(default_factory=list, description="Relevant BNS/IPC/Consumer/IT Act sections")
    next_steps: List[str] = Field(default_factory=list, description="Concrete next steps the citizen should take")
    free_legal_aid_applicable: bool = Field(False, description="Whether user qualifies for free NALSA assistance")
    disclaimer: str = Field(
        "Disclaimer: NyayaSetu AI provides legal information and educational assistance, not formal attorney representation.",
        description="Statutory legal disclaimer"
    )

# ================= Legal Drafting Schemas =================

class LegalDraftRequest(BaseModel):
    template_type: str = Field(
        ...,
        description="Type of draft: 'unpaid_salary_notice', 'rent_deposit_notice', 'consumer_complaint', 'rti_application', 'cease_and_desist'"
    )
    sender_name: str = Field(..., description="Full name of claimant/sender")
    sender_address: str = Field(..., description="Address of claimant")
    recipient_name: str = Field(..., description="Name of opposing party, company, or PIO")
    recipient_address: str = Field(..., description="Address of opposing party")
    details: Dict[str, Any] = Field(..., description="Case details such as amount owed, dates, specific grievances")
    language: str = Field("en", description="'en', 'hi', or 'gu'")

class LegalDraftResponse(BaseModel):
    template_type: str = Field(..., description="Selected draft template")
    subject: str = Field(..., description="Legal subject line")
    draft_body: str = Field(..., description="Full formal legal document formatted and ready to print/send")
    statutory_notice_period_days: int = Field(..., description="Legal response time required (e.g. 15 or 30 days)")
    legal_references: List[str] = Field(default_factory=list, description="Statutes and sections cited in the notice")
    dispatch_guidelines: List[str] = Field(default_factory=list, description="Instructions on how to send via Speed Post / Regd AD")

# ================= Legal Aid Directory Schemas =================

class LegalAidClinic(BaseModel):
    id: str
    name: str
    state: str
    district: str
    category: str  # DLSA, High Court Legal Services, Taluka, Specialized Clinic
    contact_number: str
    address: str
    free_services: List[str]
    eligibility_summary: str

class LegalAidSearchResponse(BaseModel):
    total_found: int
    clinics: List[LegalAidClinic]
    helpline_national: str = "15100 (NALSA National Free Legal Services Toll-Free Helpline)"
    cyber_helpline: str = "1930 (National Cyber Crime Reporting Portal)"

# ================= System & Health Schemas =================

class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    security_checks_passed: bool
    features: List[str]
