# VeritasGuard
**Multimodal Generative AI Framework for Vernacular Cyber Fraud Detection and Scam Deconstruction**

Academic RTD Open Elective · NVIDIA AI & Deep Learning · Dayananda Sagar University · Submission: **20 November 2026**.

## What it does
Users **manually** paste SMS/WhatsApp/Telegram/email text or upload a PNG/JPEG screenshot. Gemini (or optional Groq **for text only**) analyzes visible fraud indicators, explains psychological manipulation, and suggests protective steps in **English, Hindi or Hinglish**. The result is parsed and validated with **Pydantic v2**; no verification of a sender, URL, QR destination, or real account happens automatically. An explicitly labeled offline synthetic demo works without API access.

## Key technology
- Python, Streamlit, Pillow, Pydantic v2, python-dotenv, pytest
- Google **google-genai** SDK for text and native image reasoning
- **langchain-core** (`ChatPromptTemplate` and `RunnableLambda`) for a real single-call **text** prompt→LLM→Pydantic pipeline
- Optional **Groq** Python SDK with `openai/gpt-oss-120b` (text only; requires a second API key)
- Zero-shot and 3-example few-shot prompts; project-defined Indian fraud taxonomy

## Install and run on Windows PowerShell
```powershell
cd "D:\Project\Open Elective Project\VeritasGuard"
# Use your existing .venv; create it only if it does not already exist:
if (!(Test-Path .venv)) { py -3.12 -m venv .venv }
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v -s
.\.venv\Scripts\python.exe -m streamlit run app.py
```
Open http://localhost:8501. Preserve your existing **`.env`** during any ZIP updates; never publish it.

## Local `.env` settings
```dotenv
GEMINI_API_KEY=your_actual_google_key
GEMINI_MODEL=gemini-3.8-flash
# Optional — text only (separate provider and separate privacy policy)
GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-120b
```
Only `GEMINI_API_KEY` is needed for Gemini. Groq is disabled when its key is absent. Use the provider selector in the UI to select Groq text analysis. An explicit optional checkbox allows one text fallback from Gemini when Gemini is unavailable or rate-limited; screenshot data is **never** routed to Groq. Neither provider is called automatically in the background. Cloud free-tier limits may change.

## Features
- Text or screenshot input, manual Analyze action; screenshot orientation correction, dimension/file-size checks, metadata stripping, image preview
- Gemini vision can read **visible** screenshots, including apparent QR-payment *context*, but does not decode or verify QR payment destinations
- English, Hindi (Devanagari), Hinglish (Romanized Hindi-English) output controls
- LangChain text prompt templates, one structured LLM call, optional synthetic few-shot examples
- Risk levels: `Low`, `Moderate`, `Critical`, `Uncertain` (not proof/guarantee)
- Explainable red flags, manipulation cues, observed evidence vs unverified assumptions, plain-language actions, optional provider attribution
- National Cyber Crime Reporting Portal https://cybercrime.gov.in/ and helpline **1930**
- Pydantic-validated JSON inspector and clearly labeled synthetic offline demo

## Important limitations
- A model may misunderstand visible text, hallucinate facts, misclassify scams, and miss prompt injection attempts. Pydantic validates data **shape**, not truth.
- No sender/domain reputation lookup, QR payload decoding, payment execution, automatic message interception, live cybersecurity intelligence, or user accounts.
- Input contents go to Google or Groq only after user submits; image metadata removal is **not** visual redaction. Remove private details yourself before uploading.
- LangChain is used for **text** orchestration; image analysis remains in the native Gemini SDK to preserve multimodal support.
- Only automated mock tests can run without external API quotas. A user must test real Groq and combined live workflows separately with their own credentials.

## Project structure
- `app.py`: Streamlit interface and results renderer
- `analyzer.py`: Gemini/Groq text analyzers, prompt strategies, LangChain pipeline, offline demo
- `image_analyzer.py`: safe image preparation and Gemini native vision call
- `schema.py`: Pydantic v2 structured outputs
- `taxonomy.py`: **project-defined**, non-official scam categories
- `tests/`: mocked regressions (no live API calls)
- `docs/`: architecture, methodology, synopsis compliance, testing guide

See `docs/SYSTEM_ARCHITECTURE.md`, `docs/METHODOLOGY.md`, `docs/SYNOPSIS_COMPLIANCE.md`, `docs/TESTING_GUIDE.md`, and `WINDOWS_INTEGRATION.md` for the current implementation and verification plan.
