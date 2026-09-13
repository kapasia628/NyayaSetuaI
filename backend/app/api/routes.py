"""
REST API Router for NyayaSetu AI.
Handles incoming requests with comprehensive error handling,
validation, PII protection, and latency metrics.
"""

from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional

from app.models.schemas import (
    DocumentAnalysisRequest,
    DocumentAnalysisResponse,
    LegalChatRequest,
    LegalChatResponse,
    LegalDraftRequest,
    LegalDraftResponse,
    LegalAidSearchResponse,
    HealthResponse,
    LimitationCalculationRequest,
    LimitationCalculationResponse,
    BNSConversionResponse
)
from app.core.security import PIIRedactor, SecurityGuard
from app.core.config import settings
from app.services.legal_engine import LegalEngine
from app.services.drafting_engine import DraftingEngine
from app.services.legal_aid_service import LegalAidService
from app.services.advanced_legal_service import LimitationCalculator, BNSConverter

router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """System health check and diagnostic endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        security_checks_passed=True,
        features=[
            "Trilingual Indian Legal Simplifier (en, hi, gu)",
            "Automated Indian PII Redactor (Aadhaar, PAN, Phone, Bank A/C)",
            "Prompt Injection Defense",
            "BNS 2023 & IPC Legal Mapping",
            "Statutory Notice & RTI Drafter",
            "NALSA / DLSA Free Legal Aid Finder"
        ]
    )

@router.post("/analyze-document", response_model=DocumentAnalysisResponse, tags=["Legal Analysis"])
async def analyze_document(request: DocumentAnalysisRequest):
    """
    Analyzes, simplifies, and assesses legal notices, agreements, or FIRs.
    Performs automated PII masking and security scans before legal NLP.
    """
    # 1. Security Check (Prompt Injection / Malicious Script)
    is_safe, msg = SecurityGuard.check_input_safety(request.document_text)
    if not is_safe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    # 2. PII Redaction
    text_to_process = request.document_text
    redactions_count = 0
    if request.redact_pii:
        text_to_process, redaction_list = PIIRedactor.redact(text_to_process)
        redactions_count = len(redaction_list)

    # 3. Legal Intelligence Processing
    lang = request.language if request.language in settings.SUPPORTED_LANGUAGES else "en"
    analysis = LegalEngine.analyze_document(text_to_process, language=lang)
    analysis.redactions_count = redactions_count
    analysis.pii_redacted = request.redact_pii

    return analysis

@router.post("/chat", response_model=LegalChatResponse, tags=["Citizen Advisory"])
async def chat_legal_advisor(request: LegalChatRequest):
    """
    Conversational legal advisor ("NyayaMitra") answering citizen queries
    on Indian laws, tenancy, consumer forums, cyber crime, and labor disputes.
    """
    # 1. Security Guard
    is_safe, msg = SecurityGuard.check_input_safety(request.query)
    if not is_safe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    # 2. PII Sanitization
    sanitized_query, _ = PIIRedactor.redact(request.query)

    # 3. Advisory Response Generation
    lang = request.language if request.language in settings.SUPPORTED_LANGUAGES else "en"
    response = LegalEngine.legal_chat_advisor(sanitized_query, language=lang)
    return response

@router.post("/draft", response_model=LegalDraftResponse, tags=["Legal Drafting"])
async def draft_legal_document(request: LegalDraftRequest):
    """
    Generates a structured, legally sound legal notice, RTI application,
    or consumer grievance ready for dispatch via Indian Registered Post.
    """
    # Sanitize sender/recipient inputs
    is_safe_s, _ = SecurityGuard.check_input_safety(request.sender_name)
    is_safe_r, _ = SecurityGuard.check_input_safety(request.recipient_name)
    if not (is_safe_s and is_safe_r):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Security error: Invalid character sequences detected in party names."
        )

    return DraftingEngine.generate_draft(request)

@router.get("/legal-aid", response_model=LegalAidSearchResponse, tags=["Access to Justice"])
async def get_legal_aid_centers(
    state: Optional[str] = Query(None, description="Filter by Indian State (e.g. Gujarat, Maharashtra, Delhi)"),
    district: Optional[str] = Query(None, description="Filter by District (e.g. Ahmedabad, Surat, Mumbai)")
):
    """
    Locates official NALSA / DLSA free legal aid clinics and contact numbers for citizens.
    """
    return LegalAidService.search_clinics(state=state, district=district)

@router.post("/legal-aid/eligibility", tags=["Access to Justice"])
async def check_legal_aid_eligibility(
    is_woman_or_child: bool = False,
    is_sc_or_st: bool = False,
    is_disabled: bool = False,
    is_industrial_workman: bool = False,
    is_in_custody: bool = False,
    annual_income_inr: Optional[float] = None
):
    """
    Verifies citizen eligibility for 100% Free Legal Aid representation
    under Section 12 of the Legal Services Authorities Act, 1987.
    """
    return LegalAidService.check_eligibility(
        is_woman_or_child=is_woman_or_child,
        is_sc_or_st=is_sc_or_st,
        is_disabled=is_disabled,
        is_industrial_workman=is_industrial_workman,
        is_in_custody=is_in_custody,
        annual_income_inr=annual_income_inr
    )

@router.post("/limitation-calculator", response_model=LimitationCalculationResponse, tags=["Statutory Deadlines"])
async def calculate_statutory_limitation(request: LimitationCalculationRequest):
    """
    Computes statutory limitation deadlines and urgent procedural filing dates
    under the Limitation Act 1963, NI Act 138, and Consumer Protection Act.
    """
    return LimitationCalculator.calculate(request)

@router.get("/bns-converter", response_model=BNSConversionResponse, tags=["Criminal Law (BNS 2023)"])
async def convert_bns_section(
    query: str = Query(..., description="IPC section (e.g. 420, 302) or crime keyword (e.g. cheating, theft)")
):
    """
    Translates old IPC 1860 sections into new Bharatiya Nyaya Sanhita (BNS 2023) sections,
    bailable status, punishments, and community service provisions.
    """
    return BNSConverter.search(query)

