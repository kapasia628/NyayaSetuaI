"""
Legal Document Drafting Engine for NyayaSetu AI.
Automates generation of legally robust, standard-compliant legal notices,
RTI applications, and consumer complaints in accordance with Indian procedural laws.
"""

from datetime import date
from typing import Dict, Any, List
from app.models.schemas import LegalDraftRequest, LegalDraftResponse

class DraftingEngine:
    """
    Template and rule-based legal drafting engine generating formal,
    court-admissible notices and statutory representations.
    """

    @classmethod
    def generate_draft(cls, req: LegalDraftRequest) -> LegalDraftResponse:
        t_type = req.template_type
        today_str = date.today().strftime("%B %d, %Y")

        if t_type == "unpaid_salary_notice":
            return cls._draft_salary_notice(req, today_str)
        elif t_type == "rent_deposit_notice":
            return cls._draft_rent_deposit_notice(req, today_str)
        elif t_type == "consumer_complaint":
            return cls._draft_consumer_notice(req, today_str)
        elif t_type == "rti_application":
            return cls._draft_rti_application(req, today_str)
        elif t_type == "cease_and_desist":
            return cls._draft_cease_and_desist(req, today_str)
        else:
            return cls._draft_general_notice(req, today_str)

    @classmethod
    def _draft_salary_notice(cls, req: LegalDraftRequest, today: str) -> LegalDraftResponse:
        d = req.details
        amount = d.get("amount_owed", "[Amount in INR]")
        duration = d.get("work_duration", "[Employment Period]")
        designation = d.get("designation", "Employee")
        company = req.recipient_name

        subject = f"LEGAL NOTICE FOR RECOVERY OF OUTSTANDING SALARY AND DUES OF INR {amount}/- UNDER PAYMENT OF WAGES ACT & CONTRACT ACT"

        body = f"""VIA REGISTERED POST WITH ACKNOWLEDGEMENT DUE / SPEED POST

Date: {today}

TO:
{req.recipient_name}
{req.recipient_address}

FROM:
{req.sender_name}
{req.sender_address}

SUBJECT: {subject}

Sir/Madam,

Under instructions and on behalf of my client/claimant, {req.sender_name}, residing at {req.sender_address}, this formal Legal Notice is hereby served upon you as follows:

1. That the Claimant was employed with your esteemed organization, {company}, as '{designation}' during the tenure {duration}.

2. That the Claimant diligently, faithfully, and conscientiously performed all duties assigned without any grievance, misconduct, or adverse remarks.

3. That upon resignation / tenure completion, an aggregate outstanding sum of INR {amount}/- towards earned salary, statutory bonus, full and final settlement (FnF), and reimbursements remains unlawfully unpaid by you despite multiple written reminders.

4. That your withholding of the Claimant's lawfully earned wages constitutes a willful violation of the Payment of Wages Act, 1936, the Industrial Disputes Act, 1947, and Section 73 of the Indian Contract Act, 1872, rendering you liable for civil and criminal proceedings.

NOW THEREFORE, YOU ARE HEREBY CALLED UPON to remit the entire outstanding sum of INR {amount}/- (Rupees {amount} only) directly to the Claimant within 15 (Fifteen) days from the receipt of this Notice, along with interest @ 18% per annum from the due date until final liquidation.

TAKE NOTICE that in the event of your failure or neglect to comply with this requisition within the stipulated 15-day period, the Claimant shall be constrained to initiate appropriate legal proceedings before the competent Labor Commissioner, Labour Court, or High Court under Section 33C(2) of the Industrial Disputes Act, at your sole risk, costs, and consequences.

A copy of this notice is retained in our records for judicial presentation.

Yours faithfully,

________________________
{req.sender_name}
(Claimant / Signatory)
"""
        return LegalDraftResponse(
            template_type=req.template_type,
            subject=subject,
            draft_body=body,
            statutory_notice_period_days=15,
            legal_references=[
                "Payment of Wages Act, 1936 - Section 15",
                "Industrial Disputes Act, 1947 - Section 33C(2)",
                "Indian Contract Act, 1872 - Section 73"
            ],
            dispatch_guidelines=[
                "Print on clean A4 paper.",
                "Send via India Post Registered Post with AD (Acknowledgement Due) or Speed Post.",
                "Keep postal receipt and online tracking delivery confirmation safely for court records."
            ]
        )

    @classmethod
    def _draft_rent_deposit_notice(cls, req: LegalDraftRequest, today: str) -> LegalDraftResponse:
        d = req.details
        deposit = d.get("deposit_amount", "[Deposit Amount in INR]")
        vacated_date = d.get("vacated_date", "[Date Vacated]")
        property_addr = d.get("property_address", req.sender_address)

        subject = f"FORMAL LEGAL DEMAND NOTICE FOR REFUND OF SECURITY DEPOSIT OF INR {deposit}/- UNDER MODEL TENANCY LAWS & SECTION 73 CONTRACT ACT"

        body = f"""VIA SPEED POST WITH ACKNOWLEDGEMENT DUE

Date: {today}

TO:
{req.recipient_name} (Landlord / Lessor)
{req.recipient_address}

FROM:
{req.sender_name} (Tenant / Lessee)
{req.sender_address}

SUBJECT: {subject}

Sir/Madam,

Please take note of the following formal representation and legal demand served upon you:

1. That the undersigned, {req.sender_name}, was the bona-fide tenant of your residential/commercial premises located at: {property_addr}.

2. That at the inception of tenancy, the undersigned deposited an interest-free refundable security deposit of INR {deposit}/- (Rupees {deposit} only), receipt of which was duly acknowledged.

3. That the tenancy concluded and vacant, peaceful physical possession of the said premises was duly handed over to you on or before {vacated_date}, in clean and habitable condition, with all utility bills paid in full.

4. That despite peaceful surrender and multiple verbal and written requests, you have arbitrarily, unlawfully, and without any justifiable basis withheld the security deposit of INR {deposit}/-, which amounts to illegal enrichment, criminal breach of trust (BNS Section 316 / IPC Section 406), and breach of tenancy covenants.

YOU ARE HEREBY CALLED UPON to refund the full security deposit sum of INR {deposit}/- via NEFT/RTGS/Cheque within 15 (Fifteen) days of receipt of this notice, failing which I shall initiate:
(a) Legal proceedings before the competent Rent Authority / Tribunal under the applicable Rent Control Act;
(b) A Civil Suit for recovery of money with pendente lite and future interest at 18% p.a.;
(c) Criminal complaint for criminal breach of trust before the jurisdictional Judicial Magistrate.

Yours sincerely,

________________________
{req.sender_name}
"""
        return LegalDraftResponse(
            template_type=req.template_type,
            subject=subject,
            draft_body=body,
            statutory_notice_period_days=15,
            legal_references=[
                "Model Tenancy Act, 2021 (Provisions on Refund of Security Deposit)",
                "Indian Contract Act, 1872 - Section 73",
                "Bharatiya Nyaya Sanhita (BNS) 2023 - Section 316 (Criminal Breach of Trust)"
            ],
            dispatch_guidelines=[
                "Attach copy of the Rent Agreement, Bank Transfer/Cheque receipt of deposit, and move-out photos/keys handover receipt.",
                "Send via Registered Post / Speed Post."
            ]
        )

    @classmethod
    def _draft_consumer_notice(cls, req: LegalDraftRequest, today: str) -> LegalDraftResponse:
        d = req.details
        product = d.get("product_service_name", "[Product/Service Name]")
        cost = d.get("amount_paid", "[Amount Paid in INR]")
        defect = d.get("defect_description", "[Nature of Defect/Deficiency]")

        subject = f"LEGAL NOTICE FOR DEFICIENCY IN SERVICE & UNFAIR TRADE PRACTICE UNDER CONSUMER PROTECTION ACT, 2019"

        body = f"""VIA SPEED POST / REGISTERED E-MAIL

Date: {today}

TO:
{req.recipient_name}
{req.recipient_address}

FROM:
{req.sender_name}
{req.sender_address}

SUBJECT: {subject}

Sir/Madam,

This Legal Notice is served upon you on behalf of the consumer, {req.sender_name}:

1. That the Complainant purchased '{product}' from you on payment of INR {cost}/- vide invoice/receipt, trusting your representations of quality and service.

2. That the said product/service was discovered to be grievously defective, substandard, and unfit for use, specifically: {defect}.

3. That despite repeated complaints, service calls, and communications, you have failed and neglected to rectify the defect, provide replacement, or refund the consideration paid, which constitutes Gross Deficiency in Service under Section 2(11) and Unfair Trade Practice under Section 2(47) of the Consumer Protection Act, 2019.

NOW THEREFORE, YOU ARE CALLED UPON to:
(i) Refund the entire purchase amount of INR {cost}/- with 12% interest p.a.; OR replace the defective unit with a defect-free unit; AND
(ii) Pay INR 25,000/- towards damages for mental harassment and litigation costs, within 15 days of this notice.

Should you fail to comply, an official Consumer Complaint will be lodged before the District Consumer Disputes Redressal Commission (via E-Daakhil), claiming total compensation, punitive damages, and costs.

Yours faithfully,

________________________
{req.sender_name}
(Consumer)
"""
        return LegalDraftResponse(
            template_type=req.template_type,
            subject=subject,
            draft_body=body,
            statutory_notice_period_days=15,
            legal_references=[
                "Consumer Protection Act, 2019 - Section 2(11) (Deficiency)",
                "Consumer Protection Act, 2019 - Section 2(47) (Unfair Trade Practice)",
                "Consumer Protection Act, 2019 - Section 35 (Filing of Complaint before District Commission)"
            ],
            dispatch_guidelines=[
                "Preserve purchase invoice, warranty card, and proof of prior emails/messages.",
                "If ignored for 15 days, lodge e-complaint on http://edaakhil.nic.in"
            ]
        )

    @classmethod
    def _draft_rti_application(cls, req: LegalDraftRequest, today: str) -> LegalDraftResponse:
        d = req.details
        dept = d.get("department_name", "[Public Authority / Department]")
        info_queries = d.get("queries", [
            "1. Certified copies of the entire file notes and correspondence regarding [Subject].",
            "2. Details of action taken on representation dated [Date].",
            "3. Names and designations of officers who handled the file."
        ])
        if isinstance(info_queries, str):
            info_queries = [info_queries]

        queries_formatted = "\n".join(f"{i+1}. {q}" for i, q in enumerate(info_queries))

        subject = f"APPLICATION FOR OBTAINING INFORMATION UNDER SECTION 6(1) OF THE RIGHT TO INFORMATION (RTI) ACT, 2005"

        body = f"""FORM 'A' (See Rule 3)
APPLICATION FOR INFORMATION UNDER SECTION 6(1) OF THE RIGHT TO INFORMATION ACT, 2005

Date: {today}

TO:
The Central / State Public Information Officer (PIO / CPIO),
{req.recipient_name},
{dept},
{req.recipient_address}

FROM:
Applicant: {req.sender_name}
Address: {req.sender_address}
Citizenship: Citizen of India

SUBJECT: {subject}

Sir/Madam,

I, {req.sender_name}, am a citizen of India and hereby request you to kindly furnish the following specific information under Section 6(1) of the RTI Act, 2005:

PARTICULARS OF INFORMATION SOUGHT:
{queries_formatted}

1. Period to which the information relates: Recent / Current Financial Year.
2. Whether information is required by post or in person: By Registered Speed Post at the address mentioned above.
3. Application Fee: I have enclosed an Indian Postal Order (IPO) / Demand Draft of Rs. 10/- bearing No. ______________ payable to the Accounts Officer of your department, as prescribed under the RTI Rules. (Note: If Below Poverty Line, attach BPL card for fee exemption under Section 7(5)).

I confirm that the information sought does not fall within the exemptions specified under Section 8 or 9 of the RTI Act, 2005. Kindly furnish the requested information within the statutory period of 30 (thirty) days.

Yours faithfully,

________________________
{req.sender_name}
(Applicant)
"""
        return LegalDraftResponse(
            template_type=req.template_type,
            subject=subject,
            draft_body=body,
            statutory_notice_period_days=30,
            legal_references=[
                "Right to Information Act, 2005 - Section 6(1) (Application for information)",
                "Right to Information Act, 2005 - Section 7(1) (Mandatory 30-day response disposal)",
                "Right to Information Act, 2005 - Section 19(1) (First Appeal before Appellate Authority)"
            ],
            dispatch_guidelines=[
                "Attach a Rs. 10 Indian Postal Order (IPO) or court fee stamp as per state rules.",
                "Send to the Public Information Officer (PIO) via Speed Post.",
                "If no reply within 30 days, file First Appeal under Section 19(1) within 30 days thereafter."
            ]
        )

    @classmethod
    def _draft_cease_and_desist(cls, req: LegalDraftRequest, today: str) -> LegalDraftResponse:
        d = req.details
        act = d.get("unlawful_act", "[Harassment / Defamation / Trademark Infringement]")

        subject = f"CEASE AND DESIST LEGAL NOTICE UNDER BHARATIYA NYAYA SANHITA (BNS) & CIVIL LAW"

        body = f"""VIA REGISTERED POST AD & ELECTRONIC TRANSMISSION

Date: {today}

TO:
{req.recipient_name}
{req.recipient_address}

FROM:
{req.sender_name}
{req.sender_address}

SUBJECT: {subject}

Sir/Madam,

This Cease and Desist Legal Notice is issued to you as follows:

1. That you have been engaging in unauthorized, illegal, and tortious acts against {req.sender_name}, specifically: {act}.

2. That your conduct has caused substantial financial harm, irreparable reputational damage, and intense mental agony to the undersigned.

3. That your ongoing actions constitute an offense under Bharatiya Nyaya Sanhita (BNS) 2023 (including Section 356 for Defamation / Section 351 for Criminal Intimidation) and common law tort principles.

YOU ARE HEREBY FORMALLY CALLED UPON TO:
(a) Immediately cease and desist from continuing all such unlawful, defamatory, or infringing acts;
(b) Issue an unconditional written apology and retraction within 7 (Seven) days;
(c) Provide written confirmation that all unauthorized materials or defamatory communications have been permanently deleted and retracted.

Failing strict compliance within 7 days, appropriate criminal and civil proceedings seeking injunctive relief and damages shall be instituted against you without further reference.

Yours faithfully,

________________________
{req.sender_name}
"""
        return LegalDraftResponse(
            template_type=req.template_type,
            subject=subject,
            draft_body=body,
            statutory_notice_period_days=7,
            legal_references=[
                "Bharatiya Nyaya Sanhita (BNS), 2023 - Section 356 (Defamation)",
                "Bharatiya Nyaya Sanhita (BNS), 2023 - Section 351 (Criminal Intimidation)",
                "Civil Procedure Code, 1908 - Order 39 (Temporary Injunctions)"
            ],
            dispatch_guidelines=[
                "Serve via Registered Post and also via email / WhatsApp to establish immediate notice delivery.",
                "Retain proof of delivery."
            ]
        )

    @classmethod
    def _draft_general_notice(cls, req: LegalDraftRequest, today: str) -> LegalDraftResponse:
        subject = f"FORMAL STATUTORY LEGAL NOTICE"
        body = f"Date: {today}\n\nTO: {req.recipient_name}\nFROM: {req.sender_name}\n\nSubject: {subject}\n\nTake notice to remedy the grievance within 15 days."
        return LegalDraftResponse(
            template_type="general",
            subject=subject,
            draft_body=body,
            statutory_notice_period_days=15,
            legal_references=["Civil Procedure Code, 1908", "Indian Contract Act, 1872"],
            dispatch_guidelines=["Send via Registered Post with Acknowledgment Due."]
        )
