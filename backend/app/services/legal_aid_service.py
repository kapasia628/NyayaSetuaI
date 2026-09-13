"""
Free Legal Aid Services & DLSA Directory for NyayaSetu AI.
Implements directory search and eligibility checking under
Section 12 of the Legal Services Authorities Act, 1987 (NALSA / SLSA / DLSA).
"""

from typing import List, Optional
from app.models.schemas import LegalAidClinic, LegalAidSearchResponse

# Comprehensive preloaded directory of legal aid authorities across major Indian jurisdictions
LEGAL_AID_DIRECTORY: List[LegalAidClinic] = [
    # Gujarat
    LegalAidClinic(
        id="GSLSA-001",
        name="Gujarat State Legal Services Authority (GSLSA)",
        state="Gujarat",
        district="Ahmedabad",
        category="State Authority (High Court)",
        contact_number="079-27664978 / 15100",
        address="Gujarat High Court Complex, Sola, Ahmedabad - 380060",
        free_services=["Free Advocate Representation", "Lok Adalat Dispute Settlement", "Legal Counseling", "Bail Assistance"],
        eligibility_summary="Women, Children, SC/ST, Industrial Workmen, Disabled persons, and citizens with annual income below Rs. 1,00,000."
    ),
    LegalAidClinic(
        id="DLSA-AHM-002",
        name="District Legal Services Authority (DLSA) Ahmedabad Rural & City",
        state="Gujarat",
        district="Ahmedabad",
        category="District Legal Services Authority",
        contact_number="079-27552554",
        address="District & Sessions Court, Mirzapur, Ahmedabad - 380001",
        free_services=["Free Defense Counsel", "Legal Advice Clinic", "Victim Compensation Assistance"],
        eligibility_summary="Free for all women, children, under-trials, and persons with annual income under Rs. 1 Lakh."
    ),
    LegalAidClinic(
        id="DLSA-SUR-003",
        name="District Legal Services Authority (DLSA) Surat",
        state="Gujarat",
        district="Surat",
        category="District Legal Services Authority",
        contact_number="0261-2651441",
        address="District Court Building, Athwalines, Surat - 395001",
        free_services=["Legal Advice Clinic", "Lok Adalat Pre-litigation", "Domestic Violence Legal Help"],
        eligibility_summary="Free for women, senior citizens, marginalized communities, and indigent persons."
    ),
    LegalAidClinic(
        id="DLSA-VAD-004",
        name="District Legal Services Authority (DLSA) Vadodara",
        state="Gujarat",
        district="Vadodara",
        category="District Legal Services Authority",
        contact_number="0265-2431200",
        address="Nyay Mandir / District Court Campus, Vadodara - 390001",
        free_services=["Free Legal Aid Panel Lawyers", "Mediation Center", "Consumer Assistance"],
        eligibility_summary="All eligible persons under Section 12 of LSA Act 1987."
    ),
    LegalAidClinic(
        id="DLSA-RAK-005",
        name="District Legal Services Authority (DLSA) Rajkot",
        state="Gujarat",
        district="Rajkot",
        category="District Legal Services Authority",
        contact_number="0281-2475066",
        address="District Court Campus, Rajkot - 360001",
        free_services=["Legal Counseling", "Bail Drafting", "Labour Dispute Representation"],
        eligibility_summary="Free for workers, women, children, and persons under statutory income thresholds."
    ),
    # Maharashtra
    LegalAidClinic(
        id="MSLSA-MUM-006",
        name="Maharashtra State Legal Services Authority (MSLSA)",
        state="Maharashtra",
        district="Mumbai",
        category="State Authority (High Court)",
        contact_number="022-22691395 / 15100",
        address="105, High Court PWD Building, Fort, Mumbai - 400032",
        free_services=["Free High Court Advocates", "Mediation Services", "Undertrial Prisoner Relief"],
        eligibility_summary="Annual income up to Rs. 3,00,000 in Maharashtra; automatically free for women and SC/ST."
    ),
    # Delhi
    LegalAidClinic(
        id="DSLSA-DEL-007",
        name="Delhi State Legal Services Authority (DSLSA)",
        state="Delhi",
        district="Central Delhi",
        category="State Authority",
        contact_number="011-23384781 / 15100",
        address="Central Office, Pre-Fab Building, Patiala House Courts, New Delhi - 110001",
        free_services=["Front Office Legal Consultation", "24x7 Legal Aid Helpline", "Assistance in Rent & Domestic Disputes"],
        eligibility_summary="Free for transgender persons, women, children, SC/ST, and individuals earning under Rs. 3 Lakhs p.a."
    ),
    # Karnataka
    LegalAidClinic(
        id="KSLSA-BLR-008",
        name="Karnataka State Legal Services Authority (KSLSA)",
        state="Karnataka",
        district="Bengaluru",
        category="State Authority (High Court)",
        contact_number="080-22111725 / 15100",
        address="Nyaya Degula, 1st Floor, H. Siddaiah Road, Bengaluru - 560027",
        free_services=["Permanent Lok Adalat (Public Utilities)", "Free Legal Representation", "Labor Rights Assistance"],
        eligibility_summary="Annual income up to Rs. 3,00,000, free for women, children, and differently-abled individuals."
    )
]

class LegalAidService:
    """Service to discover nearby government legal aid authorities and verify Section 12 criteria."""

    @classmethod
    def search_clinics(cls, state: Optional[str] = None, district: Optional[str] = None) -> LegalAidSearchResponse:
        results = LEGAL_AID_DIRECTORY

        if state:
            state_clean = state.strip().lower()
            results = [c for c in results if state_clean in c.state.lower()]

        if district:
            district_clean = district.strip().lower()
            results = [c for c in results if district_clean in c.district.lower()]

        return LegalAidSearchResponse(
            total_found=len(results),
            clinics=results
        )

    @classmethod
    def check_eligibility(
        cls,
        is_woman_or_child: bool = False,
        is_sc_or_st: bool = False,
        is_disabled: bool = False,
        is_industrial_workman: bool = False,
        is_in_custody: bool = False,
        annual_income_inr: Optional[float] = None
    ) -> dict:
        """
        Calculates statutory eligibility for 100% Free Legal Aid
        under Section 12 of the Legal Services Authorities Act, 1987.
        """
        qualified = False
        reasons = []

        if is_woman_or_child:
            qualified = True
            reasons.append("Eligible under Section 12(c): Category 'Woman or Child' (No income ceiling).")
        if is_sc_or_st:
            qualified = True
            reasons.append("Eligible under Section 12(a): Member of Scheduled Caste or Scheduled Tribe.")
        if is_disabled:
            qualified = True
            reasons.append("Eligible under Section 12(d): Differently-abled person under Rights of Persons with Disabilities Act.")
        if is_industrial_workman:
            qualified = True
            reasons.append("Eligible under Section 12(e): Industrial workman under Industrial Disputes Act.")
        if is_in_custody:
            qualified = True
            reasons.append("Eligible under Section 12(g): Person in custody or judicial remand.")
        if annual_income_inr is not None and annual_income_inr <= 100000:
            qualified = True
            reasons.append("Eligible under Section 12(h): Annual income is below statutory threshold (Rs. 1,00,000 - 3,00,000 depending on state).")

        return {
            "eligible_for_free_legal_aid": qualified,
            "statute": "Section 12, Legal Services Authorities Act, 1987",
            "qualifying_grounds": reasons if reasons else ["Income exceeds standard statutory limit; can still access subsidized mediation and counseling at DLSA."],
            "how_to_apply": "Visit your District Court DLSA Front Office or call National Free Legal Helpline 15100 with identity/income proof."
        }
