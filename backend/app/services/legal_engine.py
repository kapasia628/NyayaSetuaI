"""
Legal Analysis Engine for NyayaSetu AI.
Empowers citizens by translating dense legal contracts, notices, and FIRs
into transparent, actionable insights mapped to the Indian Legal Code (BNS, BNSS, Consumer Act, IT Act).
Supports English, Gujarati (ગુજરાતી), and Hindi (हिन्दी).
"""

import re
from typing import Dict, List, Any, Tuple
from app.models.schemas import (
    DocumentAnalysisResponse,
    ClauseRisk,
    ActionItem,
    LegalChatResponse
)

class LegalEngine:
    """
    Intelligent Indian Legal Knowledge and Analysis Service.
    Operates high-performance rule-based legal parsing with AI context synthesis.
    """

    # Mapping of Old IPC sections to New BNS (Bharatiya Nyaya Sanhita) 2023 sections
    BNS_MAPPINGS = {
        "420": {"title": "Cheating / Fraud", "new_section": "BNS Section 318(4)", "old": "IPC Section 420"},
        "302": {"title": "Murder", "new_section": "BNS Section 103", "old": "IPC Section 302"},
        "378": {"title": "Theft", "new_section": "BNS Section 303", "old": "IPC Section 378/379"},
        "499": {"title": "Defamation", "new_section": "BNS Section 356", "old": "IPC Section 499/500"},
        "120B": {"title": "Criminal Conspiracy", "new_section": "BNS Section 61", "old": "IPC Section 120B"},
        "406": {"title": "Criminal Breach of Trust", "new_section": "BNS Section 316", "old": "IPC Section 406"},
        "354": {"title": "Assault/Modesty of Woman", "new_section": "BNS Section 74/75", "old": "IPC Section 354"},
        "506": {"title": "Criminal Intimidation", "new_section": "BNS Section 351", "old": "IPC Section 506"},
    }

    # Document type detection heuristics
    DOC_TYPES = [
        {"type": "Legal Notice (Demand / Eviction / Defamation)", "keywords": ["legal notice", "under instructions", "hereby call upon", "cease and desist", "failure to comply"]},
        {"type": "Rental / Lease Agreement", "keywords": ["tenancy", "lessor", "lessee", "security deposit", "premises", "monthly rent", "lock-in period"]},
        {"type": "Employment / Work Contract", "keywords": ["employer", "employee", "probation", "non-compete", "salary", "termination notice", "confidentiality"]},
        {"type": "Loan / Banking Agreement", "keywords": ["borrower", "lender", "repayment", "interest rate", "default", "hypothecation", "sarfaesi", "equated monthly installment"]},
        {"type": "Consumer Dispute / Warranty", "keywords": ["deficiency of service", "defective goods", "warranty", "refund", "unfair trade practice", "consumer court"]},
        {"type": "Cyber Crime / Online Fraud", "keywords": ["phishing", "unauthorized transaction", "otp fraud", "cyber cell", "it act", "section 66"]},
        {"type": "RTI (Right to Information) Document", "keywords": ["public information officer", "rti act", "section 6", "information sought", "appellate authority"]}
    ]

    # Clause risk triggers
    RISK_PATTERNS = [
        {
            "category": "Unilateral Penalty / Liquidated Damages",
            "regex": re.compile(r"(forfeit|liquidated damages|penalty of|interest at \d{2}%|without refund)", re.I),
            "level": "HIGH",
            "explanation_en": "Allows the other party to seize funds or impose steep financial penalties without formal court assessment.",
            "explanation_hi": "यह धारा दूसरी पार्टी को अदालत के फैसले के बिना जुर्माना या पैसा जब्त करने की अनुमति देती है।",
            "explanation_gu": "આ કલમ સામી પક્ષને કોર્ટના આદેશ વિના જંગી દંડ વસૂલવા અથવા ડિપોઝિટ જપ્ત કરવાની મંજૂરી આપે છે.",
            "rec_en": "Negotiate a mutual cap on penalties or demand proof of actual sustained loss.",
            "rec_hi": "जुर्माने की सीमा तय करने की मांग करें और नुकसान का ठोस सबूत मांगें।",
            "rec_gu": "દંડની મર્યાદા નક્કી કરવા વિનંતી કરો અને થયેલા વાસ્તવિક નુકસાનના પુરાવા માંગો."
        },
        {
            "category": "One-Sided Termination Rights",
            "regex": re.compile(r"(terminate\s+(this\s+)?(agreement|contract)\s+immediately|without\s+cause|without\s+any\s+prior\s+notice)", re.I),
            "level": "HIGH",
            "explanation_en": "The opposite party retains the unilateral right to cancel the agreement without prior notice or valid cause.",
            "explanation_hi": "दूसरी पार्टी बिना किसी पूर्व सूचना या वैध कारण के अनुबंध रद्द करने का अधिकार रखती है।",
            "explanation_gu": "સામી પક્ષ કોઈપણ પૂર્વ નોટિસ કે માન્ય કારણ વગર કરાર રદ કરવાનો એકતરફી અધિકાર રાખે છે.",
            "rec_en": "Insist on mandatory 30-day prior written notice for both parties.",
            "rec_hi": "दोनों पक्षों के लिए अनिवार्य 30 दिनों की लिखित पूर्व सूचना की शर्त जोड़ें।",
            "rec_gu": "બંને પક્ષો માટે ઓછામાં ઓછી 30 દિવસની લેખિત પૂર્વ નોટિસની શરત ઉમેરાવો."
        },
        {
            "category": "Exclusive Jurisdiction / Remote Arbitration",
            "regex": re.compile(r"(exclusive jurisdiction of the courts in|arbitration in|venue of arbitration)", re.I),
            "level": "MEDIUM",
            "explanation_en": "Forces disputes to be heard in a distant city or expensive private arbitration tribunal.",
            "explanation_hi": "विवाद होने पर दूर के शहर की अदालत या महंगे निजी मध्यस्थता में जाने के लिए बाध्य करता है।",
            "explanation_gu": "વિવાદ થાય ત્યારે દૂરના શહેરની અદાલત અથવા મોંઘી આર્બિટ્રેશન પ્રક્રિયામાં જવાની ફરજ પાડે છે.",
            "rec_en": "Seek jurisdiction where the property or cause of action actually arose.",
            "rec_hi": "अपने गृह नगर या जहाँ काम हुआ है वहाँ का क्षेत्राधिकार मांगें।",
            "rec_gu": "જ્યાં મિલકત આવેલી હોય અથવા જ્યાં ઘટના બની હોય તે સ્થાનિક કોર્ટનું અધિકારક્ષેત્ર માંગો."
        },
        {
            "category": "Non-Refundable Deposit / Forfeiture",
            "regex": re.compile(r"(non-refundable|shall not be refunded|forfeited by the owner)", re.I),
            "level": "HIGH",
            "explanation_en": "Denies return of your security deposit or advance money, violating consumer fairness principles.",
            "explanation_hi": "जमा राशि या एडवांस वापस न करने की शर्त, जो उपभोक्ता अधिकारों का हनन करती है।",
            "explanation_gu": "ડિપોઝિટ કે એડવાન્સ રકમ પરત ન કરવાનો ઇનકાર કરે છે, જે કન્ઝ્યુમર અધિકારોનું ઉલ્લંઘન છે.",
            "rec_en": "Clearly delineate refundable vs deductible items with inspection receipts.",
            "rec_gu": "પરત મળવાપાત્ર રકમ અને કાપણીના નિયમો સ્પષ્ટ લિખિતમાં નોંધો.",
            "rec_hi": "वापसी योग्य और कटौती की शर्तों को स्पष्ट रूप से लिखित में दर्ज करें।"
        },
        {
            "category": "Strict Legal Limitation / Short Notice Window",
            "regex": re.compile(r"(within\s+(7|15|thirty|30)\s+days|failing which legal action|peremptory)", re.I),
            "level": "MEDIUM",
            "explanation_en": "Requires an urgent formal written reply within a strict statutory timeframe (often 15 days).",
            "explanation_hi": "निश्चित समय सीमा (प्रायः 15 दिन) के भीतर औपचारिक लिखित उत्तर देने की मांग करता है।",
            "explanation_gu": "ચોક્કસ સમયમર્યાદા (મોટેભાગે 15 દિવસ) ની અંદર સત્તાવાર લેખિત જવાબ આપવાની માંગ કરે છે.",
            "rec_en": "Send a formal written reply via Registered Post AD or Speed Post immediately.",
            "rec_gu": "તરત જ રજિસ્ટર્ડ સ્પીડ પોસ્ટ અથવા ઈમેલ દ્વારા કાયદેસર જવાબ પાઠવો.",
            "rec_hi": "तुरंत रजिस्टर्ड स्पीड पोस्ट या ईमेल के माध्यम से औपचारिक उत्तर भेजें।"
        }
    ]

    @classmethod
    def analyze_document(cls, text: str, language: str = "en") -> DocumentAnalysisResponse:
        """
        Extracts legal classification, identifies risks, maps Indian statutes,
        and creates a citizen-centric action plan in English, Hindi, or Gujarati.
        """
        # 1. Identify Document Type
        doc_type = "General Legal Notice / Agreement"
        text_lower = text.lower()
        for candidate in cls.DOC_TYPES:
            for kw in candidate["keywords"]:
                if kw in text_lower:
                    doc_type = candidate["type"]
                    break
            if doc_type != "General Legal Notice / Agreement":
                break

        # 2. Extract Key Dates / Deadlines
        date_pattern = re.compile(r"\b(\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}|\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]+\d{4})\b", re.I)
        dates_found = list(set(date_pattern.findall(text)))[:5]
        
        # Check for notice periods (e.g., 15 days notice)
        notice_window = re.findall(r"(\d{1,2}\s+(?:days|weeks|months)\s+(?:notice|time|period))", text, re.I)
        key_dates = dates_found + list(set(notice_window))
        if not key_dates:
            key_dates = ["Statutory standard notice response window: 15 days"]

        # 3. Identify Governing Laws & BNS / Consumer Sections
        governing_laws = []
        if "notice" in text_lower:
            governing_laws.append("Section 106, Transfer of Property Act, 1882 (Notice to Quit)")
            governing_laws.append("Section 138, Negotiable Instruments Act, 1881 (Cheque Dishonour, if applicable)")
        if "rent" in text_lower or "tenant" in text_lower or "lease" in text_lower:
            governing_laws.append("Model Tenancy Act, 2021 & State Rent Control Legislations")
            governing_laws.append("Indian Contract Act, 1872 (Section 73 - Breach of Contract)")
        if "consumer" in text_lower or "defective" in text_lower or "refund" in text_lower:
            governing_laws.append("Consumer Protection Act, 2019 (Sections 2(11), 35 - Deficiency in Service)")
        if "fraud" in text_lower or "cheating" in text_lower:
            governing_laws.append("Bharatiya Nyaya Sanhita (BNS) 2023 Section 318(4) [Erstwhile IPC 420]")
            governing_laws.append("Information Technology Act, 2000 (Section 66D - Cheating by Personation using Computer)")
        if "rti" in text_lower or "information" in text_lower:
            governing_laws.append("Right to Information (RTI) Act, 2005 (Section 6 - Request for obtaining information)")
        if not governing_laws:
            governing_laws.append("Indian Contract Act, 1872 & Specific Relief Act, 1963")
            governing_laws.append("Bharatiya Nyaya Sanhita (BNS), 2023")

        # 4. Scan for Risk Clauses
        clause_risks: List[ClauseRisk] = []
        risk_points = 15  # baseline

        for rule in cls.RISK_PATTERNS:
            matches = rule["regex"].finditer(text)
            for m in matches:
                # Grab surrounding excerpt (up to 150 chars)
                start = max(0, m.start() - 40)
                end = min(len(text), m.end() + 60)
                excerpt = "..." + text[start:end].strip() + "..."

                expl = rule.get(f"explanation_{language}", rule["explanation_en"])
                rec = rule.get(f"rec_{language}", rule["rec_en"])

                clause_risks.append(ClauseRisk(
                    clause_title=rule["category"],
                    original_excerpt=excerpt,
                    risk_level=rule["level"],
                    explanation=expl,
                    recommended_action=rec
                ))

                if rule["level"] == "HIGH":
                    risk_points += 25
                elif rule["level"] == "MEDIUM":
                    risk_points += 15

        risk_score = min(98, max(20, risk_points))

        # 5. Multilingual Citizen Summary & Action Checklist
        if language == "gu":
            summary = (
                f"આ દસ્તાવેજ મુખ્યત્વે '{doc_type}' પ્રકારનો છે. "
                f"તેમાં દર્શાવેલી શરતો મુજબ તમારું એકંદર કાનૂની જોખમ સ્તર {risk_score}/100 છે. "
                f"જો આ નોટિસ હોય, તો તમારે નિયત સમયમર્યાદામાં લેખિત પ્રત્યુત્તર આપવો અત્યંત જરૂરી છે "
                f"જેથી સામી પક્ષ તમારી વિરુદ્ધ એકતરફી કાર્યવાહી ન કરી શકે."
            )
            action_plan = [
                ActionItem(step=1, action="દસ્તાવેજની તમામ તારીખો અને પુરાવાઓ (રસીદો, ઈમેલ, કરાર) સુરક્ષિત ફાઈલ કરો.", deadline="તાત્કાલિક", authority="તમારો અંગત રેકોર્ડ"),
                ActionItem(step=2, action="જો આ નોટિસ હોય, તો સમયમર્યાદા પૂરી થતાં પહેલાં લેખિત પ્રત્યુત્તર (Reply to Notice) મોકલો.", deadline="15 દિવસની અંદર", authority="સામી પક્ષ / વકીલ"),
                ActionItem(step=3, action="જો આર્થિક કે કાનૂની વિવાદ ગંભીર હોય, તો જિલ્લા કાનૂની સેવા સત્તામંડળ (DLSA) દ્વારા મફત કાનૂની સહાય મેળવો.", deadline="જરૂર મુજબ", authority="DLSA / NALSA હેલ્પલાઇન 15100")
            ]
        elif language == "hi":
            summary = (
                f"यह दस्तावेज़ मुख्य रूप से '{doc_type}' श्रेणी का है। "
                f"इसमें उल्लिखित शर्तों के आधार पर आपका कानूनी जोखिम स्तर {risk_score}/100 आंका गया है। "
                f"यदि यह कानूनी नोटिस है, तो वैधानिक समयसीमा में औपचारिक लिखित उत्तर देना अनिवार्य है ताकि दूसरी पार्टी एकतरफा कार्रवाई न कर सके।"
            )
            action_plan = [
                ActionItem(step=1, action="दस्तावेज़ की सभी मूल रसीदें, ईमेल और अनुबंध प्रतियां सुरक्षित रखें।", deadline="तत्काल", authority="व्यक्तिगत रिकॉर्ड"),
                ActionItem(step=2, action="नोटिस की मियाद समाप्त होने से पूर्व रजिस्टर्ड डाक/स्पीड पोस्ट से लिखित जवाब भेजें।", deadline="15 दिनों के भीतर", authority="विपक्षी पक्ष / अधिवक्ता"),
                ActionItem(step=3, action="यदि आप आर्थिक रूप से कमजोर हैं, तो ज़िला विधिक सेवा प्राधिकरण (DLSA) से निःशुल्क वकील सहायता लें।", deadline="यथाशीघ्र", authority="NALSA टोल-फ्री 15100")
            ]
        else:
            summary = (
                f"This document is categorized as '{doc_type}'. "
                f"Based on contractual terms and liabilities identified, the overall risk score is {risk_score}/100. "
                f"If this is an adverse legal notice, providing a timely formal written response is critical to protect your legal defense and prevent unilateral ex-parte claims."
            )
            action_plan = [
                ActionItem(step=1, action="Preserve all correspondence, transaction slips, payment receipts, and original agreements.", deadline="Immediate", authority="Personal Legal Audit Trail"),
                ActionItem(step=2, action="Issue a formal legal reply addressing factual inaccuracies under registered speed post acknowledgment.", deadline="Within 15 Days", authority="Opposing Counsel / Claimant"),
                ActionItem(step=3, action="If facing financial hardship or qualifying under Section 12, seek Free Legal Aid from District Legal Services Authority (DLSA).", deadline="As needed", authority="NALSA Helpline 15100")
            ]

        return DocumentAnalysisResponse(
            document_type=doc_type,
            summary=summary,
            key_dates=key_dates,
            governing_laws=governing_laws,
            risk_score=risk_score,
            clause_risks=clause_risks,
            action_plan=action_plan,
            pii_redacted=True,
            redactions_count=0,
            language=language
        )

    @classmethod
    def legal_chat_advisor(cls, query: str, language: str = "en") -> LegalChatResponse:
        """
        Conversational legal guidance engine mapping citizen grievances to Indian Law.
        """
        query_lower = query.lower()

        # Check for Free Legal Aid qualification
        free_legal_aid = any(term in query_lower for term in ["poor", "women", "sc", "st", "free lawyer", "no money", "laborer", "ગરીબ", "મફત વકીલ", "गरीब", "मुफ्त वकील"])

        # Intent: Security Deposit / Rent
        if any(w in query_lower for w in ["deposit", "landlord", "rent", "tenant", "ભાડું", "ડિપોઝિટ", "किराया", "मकान मालिक"]):
            if language == "gu":
                ans = (
                    "મકાનમાલિક તમારી સિક્યોરિટી ડિપોઝિટ ગેરકાયદેસર રીતે અટકાવી શકતા નથી. "
                    "મોડેલ ટેનન્સી એક્ટ અને ભારતીય કરાર ધારા હેઠળ, મકાન ખાલી કર્યા બાદ સામાન્ય ઘસારા સિવાયનું કોઈ અયોગ્ય કપાત વગર "
                    "ડિપોઝિટ પરત આપવી ફરજિયાત છે. જો મકાનમાલિક ના પાડે, તો તમે તેમને 15 દિવસની કાનૂની નોટિસ મોકલી શકો છો."
                )
            elif language == "hi":
                ans = (
                    "मकान मालिक बिना वैध कारण के आपकी सिक्योरिटी डिपॉजिट नहीं रोक सकता। "
                    "मॉडल टेनेंसी एक्ट और भारतीय अनुबंध अधिनियम के तहत, सामान्य टूट-फूट के अलावा अनुचित कटौती अवैध है। "
                    "यदि मकान मालिक पैसे वापस नहीं करता, तो आप उसे 15 दिनों का वैधानिक लीगल नोटिस भेज सकते हैं।"
                )
            else:
                ans = (
                    "Under the Model Tenancy framework and the Indian Contract Act (Section 73), a landlord cannot arbitrarily withhold your security deposit. "
                    "Ordinary wear and tear cannot be deducted. If the landlord refuses refund, the immediate legal remedy is issuing a formal 15-day Legal Notice demanding refund with interest, followed by filing a claim before the Rent Tribunal or Small Causes Court."
                )
            sections = [
                "Model Tenancy Act, 2021 (Provisions on Security Deposit Return)",
                "Indian Contract Act, 1872 - Section 73 (Compensation for Breach of Contract)"
            ]
            steps = [
                "Gather move-out handover proof, rent receipts, and chat logs.",
                "Send a formal 15-Day Legal Demand Notice via Speed Post.",
                "If unfulfilled, file an application before the Rent Authority / Rent Tribunal."
            ]

        # Intent: Unpaid Salary / Employment
        elif any(w in query_lower for w in ["salary", "unpaid", "employer", "boss", "job", "પગાર", "નોકરી", "वेतन", "नौकरी"]):
            if language == "gu":
                ans = (
                    "કંપની કે એમ્પ્લોયર તમારો મહેનતાણાનો પગાર રોકી શકતા નથી. "
                    "વેતન ચૂકવણી ધારો (Payment of Wages Act) અને શ્રમ કાયદા હેઠળ સમયસર પગાર ચૂકવવો કાનૂની જવાબદારી છે. "
                    "તમે કંપનીને 15 દિવસની લીગલ નોટિસ આપી શકો છો અથવા લેબર કમિશનર ઑફિસમાં ફરિયાદ કરી શકો છો."
                )
            elif language == "hi":
                ans = (
                    "नियोक्ता आपका अर्जित वेतन या एफएंडएफ (Full & Final) नहीं रोक सकता। "
                    "मजदूरी संदाय अधिनियम (Payment of Wages Act) के तहत यह गैरकानूनी है। "
                    "आप कंपनी को 15 दिन का लीगल नोटिस भेज सकते हैं अथवा लेबर कोर्ट/लेबर कमिश्नर कार्यालय में शिकायत दर्ज करा सकते हैं।"
                )
            else:
                ans = (
                    "Non-payment of earned wages constitutes an actionable breach of contract and violation of the Payment of Wages Act, 1936 and Industrial Disputes Act. "
                    "An employer cannot arbitrarily withhold earned salary or full-and-final settlement. You are entitled to claim the principal amount along with interest and damages."
                )
            sections = [
                "Payment of Wages Act, 1936 - Section 15",
                "Industrial Disputes Act, 1947 - Section 33C(2) (Recovery of Money from Employer)",
                "Indian Contract Act, 1872"
            ]
            steps = [
                "Compile appointment letter, salary slips, attendance records, and bank statements.",
                "Issue a formal Legal Demand Notice giving 15 days for settlement.",
                "Lodge a grievance with the District Labor Commissioner or file under Section 33C(2)."
            ]

        # Intent: Cyber Fraud / Financial Scam
        elif any(w in query_lower for w in ["scam", "fraud", "otp", "cyber", "hacked", "છેતરપિંડી", "સાયબર", "धोखाधड़ी", "साइबर"]):
            if language == "gu":
                ans = (
                    "ઓનલાઇન કે નાણાકીય છેતરપિંડીના કિસ્સામાં પ્રથમ 24 કલાક (ગોલ્ડન અવર) ખૂબ જ મહત્વપૂર્ણ છે. "
                    "તરત જ નેશનલ સાયબર હેલ્પલાઇન 1930 પર કોલ કરો જેથી તમારા ખાતામાંથી ટ્રાન્સફર થયેલા પૈસા બ્લોક કરાવી શકાય. "
                    "આ ઉપરાંત cybercrime.gov.in પર ફરિયાદ નોંધાવો."
                )
            elif language == "hi":
                ans = (
                    "साइबर या ऑनलाइन फ्रॉड होने पर पहले 24 घंटे 'गोल्डन आवर' होते हैं। "
                    "तुरंत राष्ट्रीय साइबर हेल्पलाइन 1930 पर कॉल करें ताकि ट्रांजैक्शन को फ्रीज कराया जा सके। "
                    "इसके साथ ही cybercrime.gov.in पोर्टल पर आधिकारिक ई-एफआईआर दर्ज करें।"
                )
            else:
                ans = (
                    "In financial cyber fraud, the first 24 hours constitute the 'Golden Hour'. "
                    "Dial 1930 immediately (National Cyber Crime Helpline) to initiate freeze protocols on beneficiary accounts. "
                    "File an incident report on cybercrime.gov.in and notify your bank within 3 working days for zero-liability protection under RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18."
                )
            sections = [
                "Information Technology Act, 2000 - Section 66C & 66D (Identity Theft & Impersonation)",
                "Bharatiya Nyaya Sanhita (BNS) 2023 - Section 318(4) [Cheating]",
                "RBI Circular on Customer Protection (Limiting Liability in Unauthorized Electronic Banking)"
            ]
            steps = [
                "Call 1930 immediately to block transaction routing.",
                "Lodge an official report at cybercrime.gov.in.",
                "Submit a written dispute form with bank within 72 hours."
            ]

        # Intent: Cheque Bounce
        elif any(w in query_lower for w in ["cheque", "bounce", "dishonour", "ચેક", "ચેક બાઉન્સ", "चेक बाउंस"]):
            if language == "gu":
                ans = (
                    "ચેક બાઉન્સ થવો એ નેગોશિયેબલ ઇન્સ્ટ્રુમેન્ટ્સ એક્ટની કલમ 138 હેઠળ ગંભીર ફોજદારી ગુનો છે. "
                    "બેંકમાંથી 'Cheque Return Memo' મળ્યાના 30 દિવસની અંદર સામેવાળાને 15 દિવસની ડિમાન્ડ નોટિસ મોકલવી ફરજિયાત છે. "
                    "જો તેઓ 15 દિવસમાં ચૂકવણી ન કરે, તો ત્યારપછીના 30 દિવસમાં મેજિસ્ટ્રેટ કોર્ટમાં ફરિયાદ દાખલ કરી શકાય છે."
                )
            elif language == "hi":
                ans = (
                    "चेक बाउंस होना पराक्रम्य लिखत अधिनियम (NI Act) की धारा 138 के तहत एक संज्ञेय अपराध है। "
                    "बैंक से मीमो मिलने के 30 दिनों के भीतर कानूनी नोटिस भेजना अनिवार्य है जिसमें 15 दिन का समय दिया जाता है। "
                    "यदि वे भुगतान नहीं करते हैं, तो अगले 30 दिनों में मजिस्ट्रेट कोर्ट में परिवाद दाखिल किया जा सकता है।"
                )
            else:
                ans = (
                    "Cheque dishonour for insufficiency of funds is a statutory offence under Section 138 of the Negotiable Instruments Act, 1881. "
                    "You must issue a formal Statutory Demand Notice within 30 days of receiving the Cheque Return Memo from your bank, granting 15 days to repay. If unpaid, a criminal complaint must be filed before the Judicial Magistrate within 30 days thereafter."
                )
            sections = [
                "Negotiable Instruments Act, 1881 - Section 138 (Dishonour of Cheque)",
                "Negotiable Instruments Act, 1881 - Section 143A (Interim Compensation up to 20%)"
            ]
            steps = [
                "Collect original Cheque and Bank Return Memo stating reason.",
                "Send Statutory 15-Day Demand Notice via Speed Post within 30 days.",
                "File Section 138 complaint before Metropolitan/Judicial Magistrate upon default."
            ]

        # General Legal Guidance
        else:
            if language == "gu":
                ans = (
                    "ભારતીય બંધારણ અને કાયદા અનુસાર દરેક નાગરિકને ન્યાય મેળવવાનો મૂળભૂત અધિકાર છે. "
                    "તમારા કેસમાં તથ્યો અને પુરાવાઓ સુરક્ષિત રાખવા સૌથી પહેલું પગલું છે. "
                    "જો કેસ કન્ઝ્યુમર, સિવિલ કે ક્રિમિનલ બાબતનો હોય, તો કાયદેસર નોટિસ મોકલીને અથવા સંબંધિત ફોરમમાં અરજી કરીને ન્યાય મેળવી શકાય છે."
                )
            elif language == "hi":
                ans = (
                    "भारतीय संविधान और कानून के तहत प्रत्येक नागरिक को न्याय पाने का मौलिक अधिकार है। "
                    "सर्वप्रथम मामले से संबंधित सभी दस्तावेजी साक्ष्य (रसीदें, पत्र, डिजिटल प्रमाण) सुरक्षित रखें। "
                    "विवाद की प्रकृति के अनुसार लीगल नोटिस, उपभोक्ता फोरम अथवा संबंधित विधिक प्राधिकरण में कार्रवाई की जा सकती है।"
                )
            else:
                ans = (
                    "Under the Indian Legal framework, every citizen is entitled to due process and remedies under civil, criminal, or consumer jurisdictions. "
                    "Your primary defense begins with establishing a verifiable paper trail (receipts, timestamps, digital communications). Most legal actions require serving a formal notice before approaching judicial or quasi-judicial tribunals."
                )
            sections = [
                "Constitution of India - Article 39A (Equal Justice and Free Legal Aid)",
                "Bharatiya Nyaya Sanhita (BNS), 2023",
                "Civil Procedure Code, 1908 (CPC)"
            ]
            steps = [
                "Document timeline of events with dates and witnesses.",
                "Draft and serve a formal notice specifying remedy sought.",
                "Contact NALSA Toll-Free 15100 if you require legal assistance."
            ]

        return LegalChatResponse(
            answer=ans,
            applicable_sections=sections,
            next_steps=steps,
            free_legal_aid_applicable=free_legal_aid
        )
