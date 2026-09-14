/**
 * NyayaSetu AI - Client Application Script
 * Features:
 * - Trilingual UI & Localization (English, Gujarati, Hindi)
 * - Web Speech Recognition (Voice Input in en-IN, gu-IN, hi-IN)
 * - Web Speech Synthesis (Text-to-Speech Audio Readout)
 * - WCAG 2.1 AA Accessibility & Keyboard Nav
 * - High Contrast / Dark Mode State Management
 * - Full REST API Integration for Analysis, Chat, Drafting, & Legal Aid
 */

// ================= Localization Strings =================
const I18N = {
  en: {
    appTitle: "NyayaSetu AI",
    appTagline: "Bridge to Justice & Citizen Rights",
    themeText: "Theme",
    readAloudText: "Read Aloud",
    tabSimplifier: "Legal Simplifier",
    tabChat: "NyayaMitra (Chat)",
    tabDraft: "Notice Drafter",
    tabLimitation: "Limitation & Deadlines",
    tabBns: "BNS 2023 Matrix",
    tabAid: "Free Legal Aid",
    simplifierHeading: "Document Simplifier & Risk Analyzer",
    simplifierDesc: "Paste any legal notice, lease agreement, or police notice. Our AI redacts your sensitive PII (Aadhaar, Phone, Account), translates into plain language, and highlights adverse risks.",
    pasteDocLabel: "Paste Legal Document Text:",
    uploadBtnText: "Upload File",
    speechBtnText: "Voice Input",
    sampleBtnText: "Load Sample Notice",
    piiShieldLabel: "🛡️ Enable Automated Indian PII Masking (Aadhaar, PAN, Phone numbers)",
    analyzeBtnText: "Analyze & Simplify",
    chatHeading: "NyayaMitra - Citizen AI Legal Counselor",
    chatDesc: "Ask questions in Gujarati, Hindi, or English regarding your rights under BNS 2023, Consumer Laws, Cheque Bounce, or Landlord disputes.",
    chatWelcome: "Namaste! I am NyayaMitra, your AI legal guidance assistant. You can ask me questions about rent disputes, unpaid wages, cyber scams, or court notices. How can I help you today?",
    draftHeading: "Automated Legal Notice & RTI Drafter",
    draftDesc: "Generate legally formatted, court-admissible notices and RTI applications ready to print and dispatch via Indian Speed Post.",
    limitationHeading: "Statutory Limitation & Deadline Calculator",
    limitationDesc: "Under the Limitation Act 1963 and special statutes, calculate critical legal deadlines for notice issuance and court filings.",
    bnsHeading: "Bharatiya Nyaya Sanhita (BNS 2023) vs IPC Matrix",
    bnsDesc: "Translate old Indian Penal Code (IPC 1860) sections to new BNS 2023 laws. Check bailable status, punishments, and community service provisions.",
    aidHeading: "Free Legal Aid & DLSA Locator (NALSA)",
    aidDesc: "Under Article 39A of the Indian Constitution and Section 12 of the Legal Services Authorities Act 1987, eligible citizens receive free advocate representation and dispute counseling.",
    analyzing: "Analyzing legal document with AI & redacting PII...",
    generatingDraft: "Generating formal legal draft..."
  },
  gu: {
    appTitle: "ન્યાયસેતુ AI",
    appTagline: "સામાન્ય નાગરિકો માટે સરળ કાનૂની સહાય અને ન્યાય",
    themeText: "થીમ",
    readAloudText: "વાંચી સંભળાવો",
    tabSimplifier: "દસ્તાવેજ સમજો",
    tabChat: "ન્યાયમિત્ર (ચેટ)",
    tabDraft: "નોટિસ તૈયાર કરો",
    tabLimitation: "સમયમર્યાદા (મિયાદ)",
    tabBns: "BNS 2023 કન્વર્ટર",
    tabAid: "મફત કાનૂની સહાય",
    simplifierHeading: "દસ્તાવેજ સમજો અને જોખમ ચકાસો",
    simplifierDesc: "કોઈપણ કાનૂની નોટિસ, ભાડા કરાર કે પોલીસ નોટિસ અહીં પેસ્ટ કરો. અમારું AI તમારા આધાર, ફોન નંબર સુરક્ષિત રાખીને સરળ ગુજરાતીમાં સમજાવશે.",
    pasteDocLabel: "કાનૂની દસ્તાવેજ અહીં પેસ્ટ કરો:",
    uploadBtnText: "ફાઇલ અપલોડ",
    speechBtnText: "બોલીને લખાવો",
    sampleBtnText: "નમૂનાની નોટિસ લો",
    piiShieldLabel: "🛡️ આધાર, પાન કાર્ડ અને ફોન નંબર સુરક્ષિત (માસ્ક) રાખો",
    analyzeBtnText: "વિશ્લેષણ કરો",
    chatHeading: "ન્યાયમિત્ર - તમારો AI કાનૂની સલાહકાર",
    chatDesc: "નવા ભારતીય ન્યાય સંહિતા (BNS 2023), ગ્રાહક અધિકારો, ભાડા વિવાદ કે ચેક બાઉન્સ અંગે ગુજરાતીમાં સલાહ મેળવો.",
    chatWelcome: "નમસ્તે! હું ન્યાયમિત્ર છું, તમારો કાનૂની સહાયક. તમે મને ભાડા વિવાદ, પગાર ન મળવો, ઓનલાઇન છેતરપિંડી કે કોર્ટ નોટિસ અંગે પૂછી શકો છો. હું તમને કેવી રીતે મદદ કરી શકું?",
    draftHeading: "ઓટોમેટેડ લીગલ નોટિસ અને RTI ડ્રાફ્ટર",
    draftDesc: "ભારતીય સ્પીડ પોસ્ટ દ્વારા મોકલવા માટે માન્ય અને કોર્ટમાં સ્વીકાર્ય લીગલ નોટિસ અને RTI અરજી તરત તૈયાર કરો.",
    limitationHeading: "કાનૂની સમયમર્યાદા (મિયાદ) કેલ્ક્યુલેટર",
    limitationDesc: "Limitation Act 1963 મુજબ નોટિસ મોકલવાની અને કોર્ટમાં કેસ દાખલ કરવાની આખરી તારીખો અને દિવસો ગણો.",
    bnsHeading: "ભારતીય ન્યાય સંહિતા (BNS 2023) vs IPC કન્વર્ટર",
    bnsDesc: "જૂની IPC કલમો (જેમ કે 420, 302) ને નવી BNS 2023 કલમોમાં કન્વર્ટ કરો અને જામીન તથા સમાજ સેવાના નિયમો જાણો.",
    aidHeading: "મફત કાનૂની સહાય અને DLSA કેન્દ્રો (NALSA)",
    aidDesc: "ભારતીય બંધારણની કલમ 39A અને કાનૂની સેવા સત્તામંડળ ધારાની કલમ 12 હેઠળ લાયક નાગરિકોને મફત વકીલ અને સહાય મળે છે.",
    analyzing: "દસ્તાવેજનું વિશ્લેષણ અને PII સુરક્ષા ચકાસી રહ્યા છીએ...",
    generatingDraft: "કાનૂની નોટિસ તૈયાર કરી રહ્યા છીએ..."
  },
  hi: {
    appTitle: "न्यायसेतु AI",
    appTagline: "नागरिकों के लिए सुलभ कानूनी सहायता और न्याय",
    themeText: "थीम",
    readAloudText: "सुनें (बोलकर)",
    tabSimplifier: "दस्तावेज़ सरल करें",
    tabChat: "न्यायमित्र (संवाद)",
    tabDraft: "नोटिस तैयार करें",
    tabLimitation: "समयसीमा (मियाद)",
    tabBns: "BNS 2023 मैट्रिक्स",
    tabAid: "मुफ्त कानूनी सहायता",
    simplifierHeading: "दस्तावेज़ सरलीकरण एवं जोखिम विश्लेषण",
    simplifierDesc: "कोई भी कानूनी नोटिस, किराया अनुबंध अथवा शिकायत यहाँ पेस्ट करें। हमारा AI आपके आधार व फोन नंबर को सुरक्षित रखकर सरल भाषा में समझाएगा।",
    pasteDocLabel: "कानूनी दस्तावेज़ यहाँ पेस्ट करें:",
    uploadBtnText: "फाइल अपलोड",
    speechBtnText: "बोलकर दर्ज करें",
    sampleBtnText: "सैंपल नोटिस लोड करें",
    piiShieldLabel: "🛡️ आधार, पैन एवं फोन नंबर सुरक्षा (मास्किंग) सक्षम करें",
    analyzeBtnText: "विश्लेषण करें",
    chatHeading: "न्यायमित्र - आपका AI कानूनी सलाहकार",
    chatDesc: "भारतीय न्याय संहिता (BNS 2023), उपभोक्ता अधिकार, साइबर अपराध अथवा चेक बाउंस पर हिंदी में सलाह प्राप्त करें।",
    chatWelcome: "नमस्ते! मैं न्यायमित्र हूँ, आपका AI कानूनी सहायक। आप मुझसे किराया विवाद, बकाया वेतन, साइबर फ्रॉड अथवा कानूनी नोटिस पर सवाल पूछ सकते हैं। मैं आपकी क्या मदद करूँ?",
    draftHeading: "स्वचालित लीगल नोटिस एवं RTI ड्राफ्टर",
    draftDesc: "स्पीड पोस्ट द्वारा प्रेषित किए जाने योग्य एवं न्यायालय में ग्राह्य विधिक नोटिस और आरटीआई आवेदन तुरंत तैयार करें।",
    limitationHeading: "वैधानिक परिसीमा एवं समयसीमा कैलकुलेटर",
    limitationDesc: "परिसीमा अधिनियम 1963 के तहत कानूनी नोटिस भेजने एवं न्यायालय में वाद दायर करने की महत्वपूर्ण तिथियों की गणना करें।",
    bnsHeading: "भारतीय न्याय संहिता (BNS 2023) vs IPC मैट्रिक्स",
    bnsDesc: "पुरानी आईपीसी धाराओं (जैसे 420, 302) को नई बीएनएस धाराओं में परिवर्तित करें तथा ज़मानत व सामुदायिक सेवा प्रावधान देखें।",
    aidHeading: "निःशुल्क कानूनी सहायता एवं DLSA केंद्र (NALSA)",
    aidDesc: "भारतीय संविधान के अनुच्छेद 39A एवं विधिक सेवा प्राधिकरण अधिनियम की धारा 12 के तहत पात्र नागरिकों को मुफ्त वकील सहायता उपलब्ध है।",
    analyzing: "दस्तावेज़ का विश्लेषण एवं PII सुरक्षा प्रक्रिया जारी है...",
    generatingDraft: "औपचारिक लीगल नोटिस तैयार हो रहा है..."
  }
};

// Sample Notice for 1-Click Evaluation
const SAMPLE_LEGAL_NOTICE = `
LEGAL NOTICE FOR EVICTION AND OUTSTANDING DEMAND
To: Mr. Rajesh Sharma, Tenant, Flat 402, Royal Residency, Ahmedabad.
Phone: +91 9876543210, Aadhaar: 4567 8901 2345
From: Advocate V.K. Trivedi, on behalf of Owner Mr. Suresh Patel.

Sir,
Under instructions from my client, you are hereby served this formal notice:
1. You entered into a Tenancy Agreement on 1st January 2024 for monthly rent of INR 22,000.
2. An advance security deposit of INR 66,000 was paid, which shall be strictly non-refundable and forfeited by the owner due to delayed payments.
3. You are in arrears of rent for 2 months amounting to INR 44,000.
4. You are hereby called upon to pay INR 44,000 along with liquidated damages of INR 10,000 within 15 days of this notice, failing which legal action under BNS and eviction suit shall be filed in court at your risk and cost.
`;

// App State
let currentLang = "en";
let currentTheme = "light";

// ================= Initialization =================
document.addEventListener("DOMContentLoaded", () => {
  setupLanguage();
  setupTabs();
  setupTheme();
  setupSpeechRecognition();
  setupTextToSpeech();
  setupSimplifier();
  setupFileUpload();
  setupChat();
  setupDrafting();
  setupLimitation();
  setupBNS();
  setupLegalAid();
});

// ================= Language System =================
function setupLanguage() {
  const langSelect = document.getElementById("langSelect");
  langSelect.addEventListener("change", (e) => {
    currentLang = e.target.value;
    applyLanguage(currentLang);
  });
}

function applyLanguage(lang) {
  const strings = I18N[lang] || I18N.en;

  document.getElementById("appTitle").textContent = strings.appTitle;
  document.getElementById("appTagline").textContent = strings.appTagline;
  document.getElementById("themeText").textContent = strings.themeText;
  document.getElementById("readAloudText").textContent = strings.readAloudText;

  document.getElementById("tabTitleSimplifier").textContent = strings.tabSimplifier;
  document.getElementById("tabTitleChat").textContent = strings.tabChat;
  document.getElementById("tabTitleDraft").textContent = strings.tabDraft;
  if (document.getElementById("tabTitleLimitation")) document.getElementById("tabTitleLimitation").textContent = strings.tabLimitation;
  if (document.getElementById("tabTitleBns")) document.getElementById("tabTitleBns").textContent = strings.tabBns;
  document.getElementById("tabTitleAid").textContent = strings.tabAid;

  document.getElementById("simplifierHeading").textContent = strings.simplifierHeading;
  document.getElementById("simplifierDesc").textContent = strings.simplifierDesc;
  document.getElementById("pasteDocLabel").textContent = strings.pasteDocLabel;
  if (document.getElementById("uploadBtnText")) document.getElementById("uploadBtnText").textContent = strings.uploadBtnText;
  document.getElementById("speechBtnText").textContent = strings.speechBtnText;
  document.getElementById("sampleBtnText").textContent = strings.sampleBtnText;
  document.getElementById("piiShieldLabel").textContent = strings.piiShieldLabel;
  document.getElementById("analyzeBtnText").textContent = strings.analyzeBtnText;

  document.getElementById("chatHeading").textContent = strings.chatHeading;
  document.getElementById("chatDesc").textContent = strings.chatDesc;
  document.getElementById("chatWelcomeMsg").textContent = strings.chatWelcome;

  document.getElementById("draftHeading").textContent = strings.draftHeading;
  document.getElementById("draftDesc").textContent = strings.draftDesc;

  if (document.getElementById("limitationHeading")) document.getElementById("limitationHeading").textContent = strings.limitationHeading;
  if (document.getElementById("limitationDesc")) document.getElementById("limitationDesc").textContent = strings.limitationDesc;
  if (document.getElementById("bnsHeading")) document.getElementById("bnsHeading").textContent = strings.bnsHeading;
  if (document.getElementById("bnsDesc")) document.getElementById("bnsDesc").textContent = strings.bnsDesc;

  document.getElementById("aidHeading").textContent = strings.aidHeading;
  document.getElementById("aidDesc").textContent = strings.aidDesc;
}

// ================= Tab Navigation =================
function setupTabs() {
  const tabs = [
    { btn: document.getElementById("tabBtnSimplifier"), panel: document.getElementById("tab-simplifier") },
    { btn: document.getElementById("tabBtnChat"), panel: document.getElementById("tab-chat") },
    { btn: document.getElementById("tabBtnDraft"), panel: document.getElementById("tab-draft") },
    { btn: document.getElementById("tabBtnLimitation"), panel: document.getElementById("tab-limitation") },
    { btn: document.getElementById("tabBtnBns"), panel: document.getElementById("tab-bns") },
    { btn: document.getElementById("tabBtnAid"), panel: document.getElementById("tab-aid") }
  ].filter(t => t.btn && t.panel);

  tabs.forEach(({ btn, panel }) => {
    btn.addEventListener("click", () => {
      tabs.forEach(t => {
        t.btn.classList.remove("active");
        t.btn.setAttribute("aria-selected", "false");
        t.panel.classList.remove("active");
        t.panel.hidden = true;
      });

      btn.classList.add("active");
      btn.setAttribute("aria-selected", "true");
      panel.classList.add("active");
      panel.hidden = false;
    });
  });
}

// ================= Theme & Contrast =================
function setupTheme() {
  const themeToggle = document.getElementById("themeToggle");
  themeToggle.addEventListener("click", () => {
    currentTheme = currentTheme === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", currentTheme);
    document.getElementById("themeIcon").textContent = currentTheme === "light" ? "🌓" : "☀️";
  });
}

// ================= Web Speech API (Voice Input) =================
function setupSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const speechBtn = document.getElementById("speechInputBtn");
  const chatVoiceBtn = document.getElementById("chatVoiceBtn");
  const docInput = document.getElementById("docTextInput");
  const chatInput = document.getElementById("chatInput");

  if (!SpeechRecognition) {
    if (speechBtn) speechBtn.title = "Speech recognition not supported in this browser.";
    return;
  }

  function startRecognition(targetElement, btn) {
    const recognition = new SpeechRecognition();
    recognition.lang = currentLang === "gu" ? "gu-IN" : currentLang === "hi" ? "hi-IN" : "en-IN";
    recognition.interimResults = false;

    btn.style.borderColor = "red";
    btn.classList.add("listening");

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      targetElement.value += (targetElement.value ? " " : "") + transcript;
    };

    recognition.onend = () => {
      btn.style.borderColor = "";
      btn.classList.remove("listening");
    };

    recognition.onerror = () => {
      btn.style.borderColor = "";
      btn.classList.remove("listening");
    };

    recognition.start();
  }

  if (speechBtn) {
    speechBtn.addEventListener("click", () => startRecognition(docInput, speechBtn));
  }
  if (chatVoiceBtn) {
    chatVoiceBtn.addEventListener("click", () => startRecognition(chatInput, chatVoiceBtn));
  }
}

// ================= Web Speech Synthesis (Text-to-Speech) =================
function setupTextToSpeech() {
  const ttsBtn = document.getElementById("ttsToggle");
  if (!('speechSynthesis' in window)) {
    if (ttsBtn) ttsBtn.style.display = "none";
    return;
  }

  ttsBtn.addEventListener("click", () => {
    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
      return;
    }

    // Determine readable text based on active tab
    const activePanel = document.querySelector(".tab-panel.active");
    let textToRead = "";

    if (activePanel.id === "tab-simplifier") {
      const resultCard = document.getElementById("simplifierResult");
      textToRead = resultCard.classList.contains("hidden")
        ? document.getElementById("simplifierDesc").textContent
        : resultCard.innerText;
    } else {
      textToRead = activePanel.innerText;
    }

    const utterance = new SpeechSynthesisUtterance(textToRead.slice(0, 1500));
    utterance.lang = currentLang === "gu" ? "gu-IN" : currentLang === "hi" ? "hi-IN" : "en-IN";
    window.speechSynthesis.speak(utterance);
  });
}

// ================= Tab 1: Document Simplifier Logic =================
function setupSimplifier() {
  const loadSampleBtn = document.getElementById("loadSampleBtn");
  const docInput = document.getElementById("docTextInput");
  const analyzeBtn = document.getElementById("analyzeDocBtn");
  const redactCheckbox = document.getElementById("redactPiiCheckbox");
  const resultCard = document.getElementById("simplifierResult");

  loadSampleBtn.addEventListener("click", () => {
    docInput.value = SAMPLE_LEGAL_NOTICE.trim();
  });

  analyzeBtn.addEventListener("click", async () => {
    const text = docInput.value.trim();
    if (!text) {
      alert("Please paste a legal document or click 'Load Sample Notice'.");
      return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = I18N[currentLang].analyzing || "Analyzing...";

    try {
      const res = await fetch("/api/analyze-document", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          document_text: text,
          language: currentLang,
          redact_pii: redactCheckbox.checked
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Analysis request failed.");
      }

      const data = await res.json();
      renderSimplifierResult(data, resultCard);
      resultCard.classList.remove("hidden");
      resultCard.scrollIntoView({ behavior: "smooth" });
    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      analyzeBtn.disabled = false;
      analyzeBtn.innerHTML = `🔍 <span>${I18N[currentLang].analyzeBtnText}</span>`;
    }
  });
}

function renderSimplifierResult(data, container) {
  const riskClass = data.risk_score >= 60 ? "risk-high" : "risk-medium";
  const riskLevelLabel = data.risk_score >= 60 ? "HIGH ADVERSE RISK" : "MODERATE ATTENTION REQUIRED";

  let clausesHtml = "";
  if (data.clause_risks && data.clause_risks.length > 0) {
    clausesHtml = data.clause_risks.map(c => `
      <div class="clause-item risk-item-${c.risk_level}">
        <div class="clause-title">
          <span>⚠️ ${c.clause_title}</span>
          <span class="text-xs" style="font-weight:700;">[${c.risk_level}]</span>
        </div>
        <p class="clause-excerpt">"${c.original_excerpt}"</p>
        <p class="text-sm"><strong>Explanation:</strong> ${c.explanation}</p>
        <p class="text-sm" style="color:var(--primary); font-weight:600; margin-top:0.25rem;">
          🛡️ <strong>Safeguard:</strong> ${c.recommended_action}
        </p>
      </div>
    `).join("");
  } else {
    clausesHtml = "<p class='text-muted'>No critical high-liability penalty clauses found.</p>";
  }

  let actionsHtml = "";
  if (data.action_plan && data.action_plan.length > 0) {
    actionsHtml = data.action_plan.map(a => `
      <li class="action-item-row">
        <span class="step-num">${a.step}.</span>
        <div>
          <strong>${a.action}</strong>
          <div class="text-xs text-muted">Deadline: ${a.deadline || "Standard"} &bull; Forum: ${a.authority || "Legal"}</div>
        </div>
      </li>
    `).join("");
  }

  container.innerHTML = `
    <div class="risk-banner ${riskClass}">
      <div>
        <h3 style="font-size:1.2rem; font-weight:800;">${riskLevelLabel}</h3>
        <p class="text-sm">Category: <strong>${data.document_type}</strong> | PII Redacted: <strong>${data.redactions_count} Tokens Masked</strong></p>
      </div>
      <div class="risk-score-badge">
        Risk: ${data.risk_score}/100
      </div>
    </div>

    <div class="analysis-section">
      <h3>📄 Plain Language Summary</h3>
      <p style="font-size:1.05rem; line-height:1.6;">${data.summary}</p>
    </div>

    <div class="analysis-section">
      <h3>⚖️ Applicable Laws & Statutory Codes</h3>
      <ul style="padding-left:1.25rem; font-size:0.95rem;">
        ${data.governing_laws.map(l => `<li>${l}</li>`).join("")}
      </ul>
    </div>

    <div class="analysis-section">
      <h3>⚠️ High-Risk Clauses & Protective Safeguards</h3>
      ${clausesHtml}
    </div>

    <div class="analysis-section">
      <h3>✅ Citizen Action Checklist</h3>
      <ul class="action-list">${actionsHtml}</ul>
    </div>
  `;
}

// ================= Tab 2: Legal Chat Logic =================
function setupChat() {
  const form = document.getElementById("chatForm");
  const input = document.getElementById("chatInput");
  const messagesBox = document.getElementById("chatMessages");
  const chips = document.querySelectorAll(".chip-btn");

  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      input.value = chip.getAttribute("data-query");
      form.dispatchEvent(new Event("submit"));
    });
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = input.value.trim();
    if (!query) return;

    // Add User Bubble
    appendBubble(messagesBox, "user", query);
    input.value = "";
    messagesBox.scrollTop = messagesBox.scrollHeight;

    // Add Loading Bot Bubble
    const botBubble = appendBubble(messagesBox, "bot", "Thinking...");

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: query,
          language: currentLang
        })
      });

      if (!res.ok) throw new Error("Could not process query.");
      const data = await res.json();

      let answerHtml = `<p>${data.answer}</p>`;
      if (data.applicable_sections && data.applicable_sections.length > 0) {
        answerHtml += `
          <div style="margin-top:0.5rem; font-size:0.85rem;">
            <strong>Governing Laws:</strong>
            <ul>${data.applicable_sections.map(s => `<li>${s}</li>`).join("")}</ul>
          </div>
        `;
      }
      if (data.next_steps && data.next_steps.length > 0) {
        answerHtml += `
          <div style="margin-top:0.5rem; font-size:0.85rem;">
            <strong>Immediate Steps:</strong>
            <ol style="padding-left:1rem;">${data.next_steps.map(s => `<li>${s}</li>`).join("")}</ol>
          </div>
        `;
      }
      if (data.free_legal_aid_applicable) {
        answerHtml += `
          <div style="margin-top:0.5rem; padding:0.4rem; background:var(--warning-bg); border-radius:4px; font-size:0.8rem;">
            🏛️ <strong>You may qualify for Free Legal Aid (NALSA/DLSA). Dial toll-free 15100.</strong>
          </div>
        `;
      }

      botBubble.querySelector(".bubble-body").innerHTML = answerHtml;
    } catch (err) {
      botBubble.querySelector(".bubble-body").textContent = "Error: " + err.message;
    }

    messagesBox.scrollTop = messagesBox.scrollHeight;
  });
}

function appendBubble(box, role, text) {
  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${role}-bubble`;
  bubble.innerHTML = `
    <div class="bubble-sender">${role === "user" ? "You" : "⚖️ NyayaMitra"}:</div>
    <div class="bubble-body">${text}</div>
  `;
  box.appendChild(bubble);
  return bubble;
}

// ================= Tab 3: Drafting Logic =================
function setupDrafting() {
  const form = document.getElementById("draftForm");
  const previewBox = document.getElementById("draftPreviewContent");
  const copyBtn = document.getElementById("copyDraftBtn");
  const printBtn = document.getElementById("printDraftBtn");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const tType = document.getElementById("templateSelect").value;
    const sName = document.getElementById("senderName").value;
    const sAddr = document.getElementById("senderAddress").value;
    const rName = document.getElementById("recipientName").value;
    const rAddr = document.getElementById("recipientAddress").value;
    const detailsVal = document.getElementById("caseDetails").value;

    previewBox.textContent = I18N[currentLang].generatingDraft || "Generating legal draft...";

    try {
      const res = await fetch("/api/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          template_type: tType,
          sender_name: sName,
          sender_address: sAddr,
          recipient_name: rName,
          recipient_address: rAddr,
          details: { amount_owed: detailsVal, deposit_amount: detailsVal, product_service_name: detailsVal, defect_description: detailsVal },
          language: currentLang
        })
      });

      if (!res.ok) throw new Error("Failed to draft document.");
      const data = await res.json();
      previewBox.textContent = data.draft_body;
    } catch (err) {
      previewBox.textContent = "Error: " + err.message;
    }
  });

  copyBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(previewBox.textContent)
      .then(() => alert("Draft copied to clipboard!"))
      .catch(() => alert("Failed to copy."));
  });

  printBtn.addEventListener("click", () => {
    const printWindow = window.open("", "_blank");
    printWindow.document.write(`<pre style="font-family:serif; font-size:14pt; padding:40px; white-space:pre-wrap;">${previewBox.textContent}</pre>`);
    printWindow.document.close();
    printWindow.print();
  });
}

// ================= Tab 4: Legal Aid Logic =================
function setupLegalAid() {
  const checkBtn = document.getElementById("checkEligibilityBtn");
  const resultBox = document.getElementById("eligibilityResult");
  const searchBtn = document.getElementById("searchAidBtn");
  const clinicsContainer = document.getElementById("clinicsList");

  checkBtn.addEventListener("click", async () => {
    const isWomanChild = document.getElementById("checkWomanChild").checked;
    const isScSt = document.getElementById("checkScSt").checked;
    const isWorkman = document.getElementById("checkWorkman").checked;
    const isDisabled = document.getElementById("checkDisabled").checked;
    const isLowIncome = document.getElementById("checkIncome").checked;

    const params = new URLSearchParams({
      is_woman_or_child: isWomanChild,
      is_sc_or_st: isScSt,
      is_industrial_workman: isWorkman,
      is_disabled: isDisabled,
      annual_income_inr: isLowIncome ? 90000 : 500000
    });

    try {
      const res = await fetch(`/api/legal-aid/eligibility?${params.toString()}`, { method: "POST" });
      const data = await res.json();

      resultBox.classList.remove("hidden");
      if (data.eligible_for_free_legal_aid) {
        resultBox.style.background = "var(--success-bg)";
        resultBox.style.border = "1px solid var(--success-border)";
        resultBox.style.color = "var(--success-text)";
        resultBox.innerHTML = `
          <strong>🎉 You Qualify for 100% Free Legal Representation!</strong>
          <ul style="margin:0.5rem 0 0 1rem;">${data.qualifying_grounds.map(g => `<li>${g}</li>`).join("")}</ul>
          <p style="margin-top:0.4rem;"><strong>Action:</strong> ${data.how_to_apply}</p>
        `;
      } else {
        resultBox.style.background = "var(--warning-bg)";
        resultBox.style.border = "1px solid var(--warning-border)";
        resultBox.style.color = "var(--warning-text)";
        resultBox.innerHTML = `
          <strong>Standard Paid Eligibility</strong>
          <p style="margin-top:0.25rem;">${data.qualifying_grounds[0]}</p>
        `;
      }
    } catch (err) {
      alert("Eligibility check failed: " + err.message);
    }
  });

  searchBtn.addEventListener("click", async () => {
    const state = document.getElementById("stateFilter").value;
    const district = document.getElementById("districtFilter").value;

    const params = new URLSearchParams();
    if (state) params.append("state", state);
    if (district) params.append("district", district);

    try {
      const res = await fetch(`/api/legal-aid?${params.toString()}`);
      const data = await res.json();

      if (!data.clinics || data.clinics.length === 0) {
        clinicsContainer.innerHTML = "<p class='text-muted'>No clinics found for specified location. Call National Toll-Free: <strong>15100</strong>.</p>";
        return;
      }

      clinicsContainer.innerHTML = data.clinics.map(c => `
        <div class="clinic-item">
          <div class="clinic-name">${c.name}</div>
          <div class="text-xs text-muted">${c.category} &bull; ${c.district}, ${c.state}</div>
          <div class="clinic-phone">📞 ${c.contact_number}</div>
          <div class="text-xs" style="margin-top:0.25rem;">📍 ${c.address}</div>
          <div class="text-xs" style="color:var(--success-text); margin-top:0.35rem;">
            <strong>Services:</strong> ${c.free_services.join(", ")}
          </div>
        </div>
      `).join("");
    } catch (err) {
      alert("Failed to load clinics: " + err.message);
    }
  });

  // Initial load
  searchBtn.click();
}

// ================= File Upload Support =================
function setupFileUpload() {
  const uploadBtn = document.getElementById("uploadDocBtn");
  const fileInput = document.getElementById("docFileInput");
  const docInput = document.getElementById("docTextInput");

  if (!uploadBtn || !fileInput) return;

  uploadBtn.addEventListener("click", () => fileInput.click());

  fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      docInput.value = event.target.result;
      alert(`File "${file.name}" loaded successfully into document text area!`);
    };
    reader.onerror = () => alert("Could not read file.");

    // Plain text or utf-8 parse
    reader.readAsText(file);
  });
}

// ================= Limitation & Deadline Calculator Logic =================
function setupLimitation() {
  const calcBtn = document.getElementById("calcLimitationBtn");
  const resultBox = document.getElementById("limitationResult");
  const dateInput = document.getElementById("limitationDateInput");

  // Set default date to today or 15 days ago
  if (dateInput && !dateInput.value) {
    const d = new Date();
    d.setDate(d.getDate() - 10);
    dateInput.value = d.toISOString().split("T")[0];
  }

  if (!calcBtn) return;

  calcBtn.addEventListener("click", async () => {
    const caseType = document.getElementById("limitationCaseType").value;
    const incDate = dateInput.value;

    if (!incDate) {
      alert("Please select the date of incident or memo.");
      return;
    }

    calcBtn.disabled = true;
    calcBtn.textContent = "Calculating statutory timelines...";

    try {
      const res = await fetch("/api/limitation-calculator", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          case_type: caseType,
          incident_date: incDate,
          language: currentLang
        })
      });

      if (!res.ok) throw new Error("Calculation request failed.");
      const data = await res.json();

      let stagesHtml = data.stages.map((s, idx) => {
        const badgeColor = s.status === "EXPIRED" ? "var(--danger-text)" : s.status === "URGENT" ? "var(--warning-text)" : "var(--success-text)";
        const badgeBg = s.status === "EXPIRED" ? "var(--danger-bg)" : s.status === "URGENT" ? "var(--warning-bg)" : "var(--success-bg)";
        return `
          <div class="clause-item" style="margin-bottom:1rem; border-left: 4px solid ${badgeColor};">
            <div class="clause-title">
              <span>Stage ${idx + 1}: ${s.stage_name}</span>
              <span class="text-xs" style="background:${badgeBg}; color:${badgeColor}; padding:2px 8px; border-radius:4px; font-weight:700;">
                ${s.status} (${s.days_left >= 0 ? s.days_left + " Days Left" : Math.abs(s.days_left) + " Days Expired"})
              </span>
            </div>
            <p class="text-sm text-muted">Statutory Window: ${s.statutory_timeframe}</p>
            <p class="text-sm"><strong>Statutory Deadline:</strong> <span style="font-weight:700; color:${badgeColor}">${s.deadline_date}</span></p>
            <p class="text-xs" style="margin-top:0.35rem;">ℹ️ ${s.guideline}</p>
          </div>
        `;
      }).join("");

      resultBox.innerHTML = `
        <div class="risk-banner ${data.is_expired ? 'risk-high' : 'risk-medium'}">
          <div>
            <h3 style="font-size:1.15rem; font-weight:800;">${data.is_expired ? "⚠️ LIMITATION EXPIRED / URGENT ACTION REQUIRED" : "⏱️ PROCEDURAL TIMELINE ACTIVE"}</h3>
            <p class="text-sm">Statute: <strong>${data.statute_name}</strong> | Incident Date: <strong>${data.incident_date}</strong></p>
          </div>
        </div>

        <div class="analysis-section">
          <h3>📅 Statutory Stages & Mandatory Deadlines</h3>
          ${stagesHtml}
        </div>

        <div class="analysis-section" style="background:var(--bg-surface-alt); padding:0.85rem; border-radius:8px;">
          <h4>🛡️ Legal Remedy & Delay Condonation</h4>
          <p class="text-sm">${data.remedy_notes}</p>
        </div>
      `;

      resultBox.classList.remove("hidden");
      resultBox.scrollIntoView({ behavior: "smooth" });
    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      calcBtn.disabled = false;
      calcBtn.textContent = "⚡ Calculate Statutory Deadlines & Limitation";
    }
  });
}

// ================= BNS 2023 vs IPC Matrix Logic =================
function setupBNS() {
  const searchBtn = document.getElementById("bnsSearchBtn");
  const searchInput = document.getElementById("bnsSearchInput");
  const resultsBox = document.getElementById("bnsResults");
  const chips = document.querySelectorAll(".bns-chip");

  if (!searchBtn || !searchInput) return;

  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      searchInput.value = chip.getAttribute("data-term");
      searchBtn.click();
    });
  });

  searchBtn.addEventListener("click", async () => {
    const q = searchInput.value.trim();
    if (!q) {
      alert("Please enter an IPC section or crime name (e.g. 420, 302, cheating).");
      return;
    }

    searchBtn.disabled = true;
    searchBtn.textContent = "Searching BNS database...";

    try {
      const res = await fetch(`/api/bns-converter?query=${encodeURIComponent(q)}`);
      if (!res.ok) throw new Error("Search failed.");
      const data = await res.json();

      let cardsHtml = data.matches.map(m => `
        <div class="clause-item" style="margin-bottom:1rem; border-left: 4px solid var(--primary);">
          <div class="clause-title" style="font-size:1.05rem;">
            <span>${m.offense_name}</span>
            <span class="text-xs" style="background:var(--primary-light); color:var(--primary); padding:2px 8px; border-radius:4px; font-weight:700;">
              ${m.old_ipc_section} ➔ ${m.new_bns_section}
            </span>
          </div>
          <p class="text-sm" style="margin:0.35rem 0;"><strong>Classification:</strong> ${m.classification}</p>
          <p class="text-sm"><strong>Punishment:</strong> ${m.punishment_summary}</p>
          <div class="text-xs" style="margin-top:0.4rem; padding:0.4rem; background:var(--warning-bg); border-radius:4px; color:var(--warning-text);">
            🌟 <strong>New in BNS 2023:</strong> ${m.new_provisions_bns}
          </div>
        </div>
      `).join("");

      resultsBox.innerHTML = `
        <div class="panel-header">
          <h3>BNS 2023 Results for "${data.query}" (${data.count} found)</h3>
        </div>
        ${cardsHtml}
      `;

      resultsBox.classList.remove("hidden");
      resultsBox.scrollIntoView({ behavior: "smooth" });
    } catch (err) {
      alert("Search failed: " + err.message);
    } finally {
      searchBtn.disabled = false;
      searchBtn.textContent = "Search BNS Matrix";
    }
  });
}

