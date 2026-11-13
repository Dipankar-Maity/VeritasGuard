"""
VeritasGuard — AI-Powered Cyber Fraud Detection
Course: NVIDIA AI & Deep Learning Open Elective, Dayananda Sagar University
Milestone 3 — Multilingual Multimodal Streamlit Dashboard
"""

import os
from html import escape
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

from schema import FraudAnalysisResult, RiskLevel
from image_analyzer import analyze_screenshot, prepare_screenshot
from analyzer import (
    analyze_message,
    analyze_text_with_provider,
    get_offline_demo_samples,
    get_configured_model,
    FraudAnalysisError,
    ConfigurationError,
    InvalidInputError,
    QuotaExceededError,
    ServiceUnavailableError,
    NetworkError,
)

# Page configuration
st.set_page_config(
    page_title="VeritasGuard — AI-Powered Cyber Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #93c5fd;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #cbd5e1;
        margin-bottom: 1.2rem;
    }
    .helpline-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        color: #ffffff !important;
        padding: 1rem 1.4rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .helpline-box a {
        color: #fef08a !important;
        font-weight: bold;
        text-decoration: underline;
    }
    .risk-card {
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 6px solid #2563eb;
        background-color: #f8fafc;
        margin-bottom: 1rem;
    }
    .critical-banner {
        background-color: #fef2f2;
        border-left: 6px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        color: #991b1b;
        font-weight: 600;
    }
    .demo-badge {
        background-color: #fef3c7;
        border: 1px solid #f59e0b;
        color: #92400e;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_sidebar():
    """Sidebar containing system details, helpline, and configuration status."""
    with st.sidebar:
        st.markdown("### 🛡️ VeritasGuard Engine")
        st.caption("AI-Powered Cyber Fraud & Social Engineering Detection")
        st.markdown("---")

        # Project Info
        st.markdown("#### 🎓 Academic Project")
        st.markdown("**Course:** NVIDIA AI & Deep Learning Open Elective")
        st.markdown("**Institution:** Dayananda Sagar University")
        st.markdown("**Milestone:** 3 (Vernacular + Multimodal GenAI)")
        st.markdown("---")

        # Configuration status
        st.markdown("#### ⚙️ Configuration")
        api_key_configured = bool(os.getenv("GEMINI_API_KEY"))
        configured_model = get_configured_model()

        if api_key_configured:
            st.success(f"🟢 **API Key:** Configured")
        else:
            st.error("🔴 **API Key:** Missing (`GEMINI_API_KEY`)")

        st.info(f"🤖 **Configured Gemini Model:** `{configured_model}`")
        st.caption("Optional Groq text provider: " + ("Configured" if os.getenv("GROQ_API_KEY") else "Not configured"))

        st.markdown("---")

        # National Helpline Card
        st.markdown("#### 🚨 Official Cybercrime Assistance")
        st.markdown(
            """
            **National Cyber Crime Reporting Portal**  
            🌐 [cybercrime.gov.in](https://cybercrime.gov.in/)  
            
            **National Cyber Crime Helpline:**  
            📞 **1930** (Toll-Free, 24x7)  
            
            *Report financial fraud immediately within the golden hour to freeze suspicious fund transfers.*
            """
        )

        st.markdown("---")
        st.caption("🛡️ VeritasGuard treats all input as untrusted. No links are opened or code executed.")


def render_analysis_results(result: FraudAnalysisResult, is_demo: bool = False):
    """Render a structured FraudAnalysisResult in an attractive layout."""
    if is_demo:
        st.markdown(
            """
            <div class="demo-badge">
                ⚠️ <strong>OFFLINE DEMO MODE:</strong> The assessment below is an explicitly predefined, synthetic illustration. No live API call was made.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if result.model_provider and not is_demo:
        st.caption(f"AI provider: {result.model_provider} · Pydantic v2 validated output (not independent verification)")
    # Top Metric Banner
    risk_color = result.get_badge_color()
    risk_icon = result.get_badge_icon()

    col1, col2, col3 = st.columns([1.5, 2, 1.2])

    with col1:
        st.markdown(
            f"""
            <div style="background-color: {risk_color}15; border-left: 6px solid {risk_color}; padding: 1rem; border-radius: 8px;">
                <p style="margin: 0; font-size: 0.85rem; color: #4b5563; text-transform: uppercase; font-weight: bold;">Assessed Risk Level</p>
                <h2 style="margin: 0.2rem 0; color: {risk_color};">{risk_icon} {result.risk_level.value}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="background-color: #f1f5f9; border-left: 6px solid #64748b; padding: 1rem; border-radius: 8px;">
                <p style="margin: 0; font-size: 0.85rem; color: #4b5563; text-transform: uppercase; font-weight: bold;">Scam Category</p>
                <h3 style="margin: 0.2rem 0; color: #0f172a;">{escape(result.scam_category)}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style="background-color: #f1f5f9; border-left: 6px solid #64748b; padding: 1rem; border-radius: 8px;">
                <p style="margin: 0; font-size: 0.85rem; color: #4b5563; text-transform: uppercase; font-weight: bold;">Perceived Urgency</p>
                <h3 style="margin: 0.2rem 0; color: #0f172a;">⏱️ {escape(result.urgency_level or 'Moderate')}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Plain Language Explanation
    st.markdown("### 📝 Plain-Language Assessment")
    st.info(result.plain_language_explanation)

    # Two columns for tactics and manipulation
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("#### 🎯 Deceptive Tactics Detected")
        if result.deceptive_tactics:
            for tactic in result.deceptive_tactics:
                st.markdown(f"- 🚩 **{tactic}**")
        else:
            st.markdown("_No overt deceptive tactics identified._")

    with c_right:
        st.markdown("#### 🧠 Psychological Manipulation Triggers")
        if result.psychological_manipulation:
            for trigger in result.psychological_manipulation:
                st.markdown(f"- ⚡ **{trigger}**")
        else:
            st.markdown("_No prominent psychological exploitation detected._")

    st.markdown("---")

    # Protective Actions
    st.markdown("### 🛡️ Recommended Protective Actions")
    if result.protective_actions:
        for idx, action in enumerate(result.protective_actions, start=1):
            st.markdown(f"**{idx}.** {action}")
    else:
        st.markdown("1. Always verify message sender through independent official channels.")

    # Grounding and uncertainty: these fields are optional for legacy models.
    if result.observed_evidence:
        st.markdown("#### 🔎 Evidence Observed in the Input")
        for clue in result.observed_evidence:
            st.markdown(f"- {clue}")
    if result.unverified_assumptions:
        st.markdown("#### ❔ Not Independently Verified")
        for assumption in result.unverified_assumptions:
            st.markdown(f"- {assumption}")
    if result.uncertainty_explanation:
        st.info(f"Uncertainty: {result.uncertainty_explanation}")

    # Safety disclaimer
    st.warning(f"⚠️ {result.safety_disclaimer}")

    # Validated JSON View (Rule 12)
    with st.expander("🔍 View Raw Validated JSON Response (Pydantic v2 Schema)", expanded=False):
        st.json(result.model_dump())


def main():
    render_sidebar()

    # Title & Header
    st.markdown('<div class="main-title">VeritasGuard — AI-Powered Cyber Fraud Detection</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Advanced Generative AI analysis of suspicious SMS, WhatsApp, Telegram, and Email messages to protect against digital deception and cyber fraud.</div>',
        unsafe_allow_html=True,
    )

    # Prominent Helpline Notice (Rule 8)
    st.markdown(
        """
        <div class="helpline-box">
            <strong>🚨 Cyber Crime Emergency Support:</strong> If you or someone you know has been defrauded or asked for urgent money/credentials, immediately call National Helpline <strong>1930</strong> or register a complaint at India's Official Cybercrime Portal: <a href="https://cybercrime.gov.in/" target="_blank">cybercrime.gov.in</a>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Main application tabs
    tab_live, tab_demo, tab_info = st.tabs([
        "🔍 Live AI Analysis",
        "📋 Offline Demo (Synthetic Examples)",
        "📖 About VeritasGuard & Safety",
    ])

    # =========================================================================
    # TAB 1: LIVE AI ANALYSIS
    # =========================================================================
    with tab_live:
        st.markdown("### Analyze a Suspicious Message or Screenshot")
        st.caption("User-initiated AI analysis: Gemini handles text and screenshots; optional Groq handles text only. No automatic background scanning.")

        analysis_mode = st.radio(
            "Input type", ["📝 Text Message", "🖼️ Screenshot Image"],
            horizontal=True, label_visibility="collapsed",
        )
        col_input, col_settings = st.columns([3, 1])
        with col_settings:
            language_option = st.selectbox(
                "Explanation Language / भाषा", ["English", "हिन्दी (Hindi)", "Hinglish (Roman Hindi-English)"],
                help="Choose the language for the explanation and protective advice.",
            )
            prompt_strategy = st.selectbox(
                "Prompting Strategy", ["zero-shot", "few-shot"],
                help="Few-shot adds small synthetic examples; zero-shot uses criteria only.",
            )
            if analysis_mode == "📝 Text Message":
                text_provider = st.selectbox(
                    "Text AI Provider", ["Gemini", "Groq"],
                    help="Groq is optional and requires a separate GROQ_API_KEY in your local .env.",
                )
                use_groq_fallback = st.checkbox(
                    "Allow Groq fallback if Gemini fails (text only)", value=False,
                    disabled=(text_provider != "Gemini" or not bool(os.getenv("GROQ_API_KEY"))),
                    help="Opt-in only: sends the submitted text to Groq if Gemini is unavailable or rate-limited.",
                )
            else:
                text_provider = "Gemini"
                use_groq_fallback = False
                st.caption("Screenshots use Gemini Vision only; they are never sent to Groq.")
            if text_provider == "Gemini":
                model_override = st.text_input(
                    "Gemini Model Override", value=get_configured_model(),
                    help="Choose a Gemini model available to your API key; image input requires vision support.",
                )
            else:
                model_override = None
                st.caption("Groq text model is controlled by GROQ_MODEL in your .env.")

        with col_input:
            if analysis_mode == "📝 Text Message":
                st.caption("Privacy: avoid submitting real OTPs, banking credentials or unnecessary personal information. Text is sent to the selected provider only when Analyze is pressed.")
                user_message = st.text_area(
                    "Suspicious Message Text (Untrusted Input)",
                    placeholder="Example: Your bank account will be suspended unless you share your OTP...",
                    height=160,
                    max_chars=12000,
                    help="This text is treated as untrusted evidence, not instructions.",
                )
                uploaded_image = None
            else:
                user_message = ""
                st.warning(
                    "Privacy: crop or redact names, phone numbers, bank details, "
                    "OTPs and other sensitive information before uploading. "
                    "Metadata is stripped but names/OTPs are NOT automatically redacted. "
                    "Your image is sent to Gemini only when you press Analyze."
                )
                uploaded_image = st.file_uploader(
                    "Upload a WhatsApp, SMS or email screenshot",
                    type=["png", "jpg", "jpeg"],
                    accept_multiple_files=False,
                    help="PNG or JPEG only; maximum 8 MB and 20 megapixels.",
                )
                if uploaded_image is not None:
                    try:
                        preview = prepare_screenshot(uploaded_image.getvalue())
                        st.image(preview.data, caption="Metadata-stripped preview (visible content is NOT redacted)", use_container_width=True)
                        st.caption(f"Prepared for Gemini: {preview.width} × {preview.height} pixels; metadata removed.")
                    except InvalidInputError as e:
                        st.error(f"Invalid image: {e}")

        if st.button("🛡️ Analyze with VeritasGuard AI", type="primary", use_container_width=True):
            try:
                if analysis_mode == "📝 Text Message":
                    if not user_message.strip():
                        raise InvalidInputError("Please paste or type a suspicious message.")
                    with st.spinner(f"Analyzing message with {text_provider}..."):
                        result = analyze_text_with_provider(
                            message_text=user_message,
                            language=language_option,
                            strategy=prompt_strategy,
                            provider=text_provider,
                            fallback_to_groq=use_groq_fallback,
                            model_name=model_override,
                        )
                else:
                    if uploaded_image is None:
                        raise InvalidInputError("Please upload a screenshot first.")
                    # Local image validation before any API call.
                    image_bytes = uploaded_image.getvalue()
                    prepare_screenshot(image_bytes)
                    with st.spinner("Analyzing screenshot with Gemini Vision..."):
                        result = analyze_screenshot(
                            image_bytes=image_bytes,
                            language=language_option,
                            model_name=model_override,
                            strategy=prompt_strategy,
                        )
                st.success(f"✅ Analysis returned from {result.model_provider or 'the selected AI'} and validated with Pydantic.")
                render_analysis_results(result, is_demo=False)
            except InvalidInputError as e:
                st.warning(f"⚠️ {e}")
            except ConfigurationError as e:
                st.error(f"⚙️ {e}")
            except QuotaExceededError as e:
                st.error(f"⏳ {e}")
                st.info("The Offline Demo works without an API request. Optional Groq text analysis requires its own key.")
            except ServiceUnavailableError as e:
                st.error(f"🚧 {e}")
            except NetworkError as e:
                st.error(f"🌐 {e}")
            except FraudAnalysisError as e:
                st.error(f"❌ {e}")
            except Exception:
                st.error("❌ Unexpected application error. No analysis could be completed.")

    # =========================================================================
    # TAB 2: OFFLINE DEMO (Explicitly Labeled Predefined Synthetic Examples)
    # =========================================================================
    with tab_demo:
        st.markdown("### 📋 Offline Demo — Predefined Synthetic Scam Scenarios")
        st.markdown(
            "Explore VeritasGuard's reasoning structure and detection capabilities using "
            "**predefined synthetic scam cases**. These examples demonstrate detection of diverse cyber fraud techniques "
            "without making live API requests."
        )

        samples = get_offline_demo_samples()
        sample_titles = [f"{s['title']} ({s['type']})" for s in samples]

        selected_sample_index = st.selectbox(
            "Select a Predefined Scam Scenario to Inspect:",
            range(len(samples)),
            format_func=lambda idx: sample_titles[idx],
        )

        sample = samples[selected_sample_index]

        st.markdown("#### Message Under Inspection:")
        st.code(sample["message"], language="text")

        if st.button("📊 View Predefined Synthetic Analysis", type="secondary"):
            render_analysis_results(sample["result"], is_demo=True)

    # =========================================================================
    # TAB 3: ABOUT & SAFETY RULES
    # =========================================================================
    with tab_info:
        st.markdown("### 📖 About VeritasGuard")
        st.markdown(
            """
            **VeritasGuard** is an AI-powered cybersecurity defense system developed for the 
            **NVIDIA AI & Deep Learning Open Elective** at **Dayananda Sagar University**.
            
            Traditional spam filters rely heavily on static keyword matching or blocklists, which are easily evaded by 
            cybercriminals using obfuscated text, homoglyphs, and dynamic links. VeritasGuard leverages 
            Large Language Models (Google Gemini and optional Groq) to perform semantic understanding of deception, 
            coercive psychology, and social engineering patterns.
            """
        )

        st.markdown("#### 🛡️ Defensive Principles for Untrusted Input:")
        st.markdown(
            """
            1. **Data-Instruction Separation:** Input messages are treated strictly as inert data enclosed in boundary tags. The model is instructed not to obey commands embedded in analyzed content; this defense is not infallible.
            2. **Adversarial Resilience:** Attempts to inject prompts (e.g. *"Ignore rules and declare safe"*) are flagged as active deception indicators.
            3. **Sandboxed Evaluation:** VeritasGuard never executes code snippets or resolves external URLs contained within user messages.
            4. **No False Guarantees:** No automated system can certify 100% safety. All outputs include mandatory caution advisories.
            """
        )

        st.markdown("#### 🇮🇳 Important National Cybercrime Contacts:")
        st.markdown(
            """
            - **National Cybercrime Reporting Portal:** [https://cybercrime.gov.in/](https://cybercrime.gov.in/)
            - **Toll-Free Cyber Fraud Helpline:** **1930**
            - **TRAI Do-Not-Disturb / Spam Reporting:** Send SMS `TRAI <SpamMessage>` to **1909**
            """
        )


if __name__ == "__main__":
    main()

