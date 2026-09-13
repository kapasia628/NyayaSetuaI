"""
Advanced Legal Services: Statutory Limitation Calculator & BNS 2023 Matrix.
Adheres strictly to the Limitation Act 1963, NI Act, Consumer Act 2019, and Bharatiya Nyaya Sanhita.
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Any
from app.models.schemas import (
    LimitationCalculationRequest,
    LimitationCalculationResponse,
    LimitationStage,
    BNSConversionResponse,
    BNSOffenseDetail
)

class LimitationCalculator:
    """Calculates statutory limitation periods and procedural filing deadlines under Indian law."""

    @classmethod
    def calculate(cls, req: LimitationCalculationRequest) -> LimitationCalculationResponse:
        try:
            inc_dt = datetime.strptime(req.incident_date, "%Y-%m-%d").date()
        except ValueError:
            inc_dt = date.today()

        today = date.today()
        c_type = req.case_type.lower()
        stages: List[LimitationStage] = []
        is_expired = False
        remedy_notes = ""
        statute = ""

        # Case 1: Cheque Bounce under Section 138 Negotiable Instruments Act
        if "cheque" in c_type or "138" in c_type:
            statute = "Negotiable Instruments Act, 1881 (Sections 138 & 142)"
            
            # Stage 1: Demand Notice (30 days from Bank Memo)
            d1 = inc_dt + timedelta(days=30)
            days_left_1 = (d1 - today).days
            s1_status = "EXPIRED" if days_left_1 < 0 else "URGENT" if days_left_1 <= 7 else "SAFE"
            stages.append(LimitationStage(
                stage_name="Statutory Demand Notice to Drawer",
                statutory_timeframe="30 Days from date of Bank Return Memo",
                deadline_date=d1.strftime("%Y-%m-%d"),
                days_left=days_left_1,
                status=s1_status,
                guideline="Notice must demand payment within 15 days via Registered Post / Speed Post."
            ))

            # Stage 2: Payment Window (15 days for drawer to pay)
            d2 = d1 + timedelta(days=15)
            days_left_2 = (d2 - today).days
            s2_status = "EXPIRED" if days_left_2 < 0 else "URGENT" if days_left_2 <= 5 else "SAFE"
            stages.append(LimitationStage(
                stage_name="Statutory 15-Day Payment Cure Window",
                statutory_timeframe="15 Days from receipt of legal notice",
                deadline_date=d2.strftime("%Y-%m-%d"),
                days_left=days_left_2,
                status=s2_status,
                guideline="Wait for 15 days to elapse before filing criminal case in Magistrate Court."
            ))

            # Stage 3: Magistrate Court Filing (30 days after failure)
            d3 = d2 + timedelta(days=30)
            days_left_3 = (d3 - today).days
            s3_status = "EXPIRED" if days_left_3 < 0 else "URGENT" if days_left_3 <= 7 else "SAFE"
            if days_left_3 < 0:
                is_expired = True
            stages.append(LimitationStage(
                stage_name="Criminal Complaint Filing in Judicial Magistrate Court",
                statutory_timeframe="30 Days after expiry of the 15-day notice period",
                deadline_date=d3.strftime("%Y-%m-%d"),
                days_left=days_left_3,
                status=s3_status,
                guideline="File formal complaint under Section 138 read with Section 142(1)(b) of NI Act."
            ))

            remedy_notes = (
                "Section 142(1)(b) Proviso allows the Court to condone delay if sufficient cause is shown. "
                "File an application for Condonation of Delay supported by an affidavit explaining medical or unavoidable grounds."
            )

        # Case 2: Consumer Dispute
        elif "consumer" in c_type:
            statute = "Consumer Protection Act, 2019 (Section 69)"
            d1 = inc_dt + timedelta(days=730)  # 2 years
            days_left = (d1 - today).days
            is_expired = days_left < 0
            stages.append(LimitationStage(
                stage_name="Filing before District Consumer Commission (E-Daakhil)",
                statutory_timeframe="2 Years from the date on which the cause of action arose",
                deadline_date=d1.strftime("%Y-%m-%d"),
                days_left=days_left,
                status="EXPIRED" if days_left < 0 else "URGENT" if days_left <= 30 else "SAFE",
                guideline="Lodge complaint on https://edaakhil.nic.in with purchase invoice and grievance logs."
            ))
            remedy_notes = "Section 69(2) empowers the Commission to admit a complaint after 2 years if adequate cause for delay is established."

        # Case 3: Unpaid Wages / Salary Recovery
        elif "wage" in c_type or "salary" in c_type:
            statute = "Limitation Act, 1963 (Article 7 & 113) & Payment of Wages Act, 1936"
            d1 = inc_dt + timedelta(days=1095)  # 3 years
            days_left = (d1 - today).days
            is_expired = days_left < 0
            stages.append(LimitationStage(
                stage_name="Recovery Claim before Labor Authority or Civil Suit",
                statutory_timeframe="3 Years from the date wages became due",
                deadline_date=d1.strftime("%Y-%m-%d"),
                days_left=days_left,
                status="EXPIRED" if days_left < 0 else "URGENT" if days_left <= 60 else "SAFE",
                guideline="File Section 33C(2) recovery or representation before the Labor Commissioner."
            ))
            remedy_notes = "Under Payment of Wages Act, direct claims before the Authority normally carry a 12-month limit, extendable on reasonable cause."

        # Case 4: Default / Tenancy / RTI
        else:
            statute = "Indian Limitation Act, 1963 / Model Tenancy Act"
            d1 = inc_dt + timedelta(days=365)
            days_left = (d1 - today).days
            stages.append(LimitationStage(
                stage_name="Legal Notice & Representation",
                statutory_timeframe="Statutory Limitation: 1 to 3 Years depending on tribunal",
                deadline_date=d1.strftime("%Y-%m-%d"),
                days_left=days_left,
                status="SAFE" if days_left > 30 else "URGENT",
                guideline="Issue formal legal demand notice immediately to pause limitation defenses."
            ))
            remedy_notes = "Section 5 of the Limitation Act allows delay condonation for sufficient cause in appeals and applications."

        return LimitationCalculationResponse(
            case_type=req.case_type,
            incident_date=req.incident_date,
            statute_name=statute,
            stages=stages,
            is_expired=is_expired,
            condonation_of_delay_available=True,
            remedy_notes=remedy_notes
        )


class BNSConverter:
    """Comprehensive lookup engine mapping Indian Penal Code (IPC 1860) to Bharatiya Nyaya Sanhita (BNS 2023)."""

    DATABASE: List[Dict[str, Any]] = [
        {
            "old_ipc": "IPC Section 420",
            "new_bns": "BNS Section 318(4)",
            "name": "Cheating and dishonestly inducing delivery of property",
            "classification": "Cognizable, Non-Bailable, Magistrate of the First Class",
            "punishment": "Imprisonment up to 7 years and mandatory fine",
            "new_provisions": "Enhanced definition of digital financial deception and electronic property fraud."
        },
        {
            "old_ipc": "IPC Section 302",
            "new_bns": "BNS Section 103(1) & 103(2)",
            "name": "Punishment for Murder / Mob Lynching",
            "classification": "Cognizable, Non-Bailable, Court of Session",
            "punishment": "Death or imprisonment for life, and fine",
            "new_provisions": "Section 103(2) introduces explicit statutory punishment (Death / Life Imprisonment) for mob lynching on grounds of race, caste, or community."
        },
        {
            "old_ipc": "IPC Section 378 / 379",
            "new_bns": "BNS Section 303(1) & 303(2)",
            "name": "Theft (Snatching & Petty Offenses)",
            "classification": "Cognizable, Non-Bailable",
            "punishment": "Imprisonment up to 3 years, or fine, or both. Section 303(2) proviso adds Community Service for first-time petty theft under Rs. 5,000.",
            "new_provisions": "First-time inclusion of Community Service as a statutory alternative to imprisonment for petty theft."
        },
        {
            "old_ipc": "IPC Section 499 / 500",
            "new_bns": "BNS Section 356",
            "name": "Defamation",
            "classification": "Non-Cognizable, Bailable, Magistrate of the First Class",
            "punishment": "Simple imprisonment up to 2 years, or with fine, or with both, or with Community Service.",
            "new_provisions": "Permits magistrate to order Community Service instead of prison."
        },
        {
            "old_ipc": "IPC Section 120B",
            "new_bns": "BNS Section 61",
            "name": "Criminal Conspiracy",
            "classification": "Cognizable / Non-Bailable depending on offense conspired",
            "punishment": "Same manner as if the person had abetted such offense.",
            "new_provisions": "Streamlined alongside general inchoate offenses."
        },
        {
            "old_ipc": "IPC Section 304A",
            "new_bns": "BNS Section 106",
            "name": "Causing death by negligence / Hit and Run",
            "classification": "Cognizable, Bailable (General) / Non-Bailable (Hit and Run)",
            "punishment": "Up to 5 years for general negligence; up to 10 years imprisonment for escaping the scene without reporting (Hit and Run).",
            "new_provisions": "Severe 10-year penalty introduced under Section 106(2) for motorists fleeing the scene without reporting to police."
        },
        {
            "old_ipc": "IPC Section 354",
            "new_bns": "BNS Section 74 / 75",
            "name": "Assault or criminal force to woman with intent to outrage modesty",
            "classification": "Cognizable, Non-Bailable",
            "punishment": "Imprisonment not less than 1 year which may extend to 5 years, and fine.",
            "new_provisions": "Enhanced victim protection, digital audio-video recording mandates under BNSS."
        },
        {
            "old_ipc": "IPC Section 506",
            "new_bns": "BNS Section 351",
            "name": "Criminal Intimidation",
            "classification": "Non-Cognizable / Cognizable, Bailable",
            "punishment": "Imprisonment up to 2 years, or fine, or both (Up to 7 years if threat is of death/grievous hurt).",
            "new_provisions": "Explicitly encompasses intimidation executed via electronic, encrypted, or digital channels."
        }
    ]

    @classmethod
    def search(cls, query: str) -> BNSConversionResponse:
        q = query.strip().lower()
        results: List[BNSOffenseDetail] = []

        for item in cls.DATABASE:
            # Check matching old section, new section, or name
            if (
                q in item["old_ipc"].lower()
                or q in item["new_bns"].lower()
                or q in item["name"].lower()
                or (q.isdigit() and q in item["old_ipc"])
            ):
                results.append(BNSOffenseDetail(
                    old_ipc_section=item["old_ipc"],
                    new_bns_section=item["new_bns"],
                    offense_name=item["name"],
                    classification=item["classification"],
                    punishment_summary=item["punishment"],
                    new_provisions_bns=item["new_provisions"]
                ))

        # If nothing exact found, return top general results
        if not results:
            results = [
                BNSOffenseDetail(
                    old_ipc_section=item["old_ipc"],
                    new_bns_section=item["new_bns"],
                    offense_name=item["name"],
                    classification=item["classification"],
                    punishment_summary=item["punishment"],
                    new_provisions_bns=item["new_provisions"]
                )
                for item in cls.DATABASE[:3]
            ]

        return BNSConversionResponse(
            query=query,
            matches=results,
            count=len(results)
        )
