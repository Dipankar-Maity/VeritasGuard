# VeritasGuard

**Multimodal Generative AI Framework for Vernacular Cyber Fraud Detection and Scam Deconstruction**

Academic Ready to Deploy (RTD) Open Elective project · NVIDIA AI & Deep Learning · Dayananda Sagar University  
**Developed by:** Dipankar Kumar Maity · **USN:** SCA25MCA097  
**Submission:** 20 November 2026

## Overview

VeritasGuard is a Streamlit-based educational cyber-fraud analysis tool. Users manually paste suspicious SMS, WhatsApp, Telegram, or email text, or upload a PNG/JPEG screenshot. Google Gemini analyzes text and screenshots; an optional Groq provider can analyze **text only**. The application highlights suspicious patterns and psychological tactics, provides protective suggestions in **English, Hindi, or Hinglish**, and validates the shape of its AI responses using **Pydantic v2**.

VeritasGuard is **not** an automated security scanner. It does not independently authenticate senders, verify web links, decode or verify QR payment destinations, inspect bank accounts, or guarantee that a message is safe. An explicitly labeled offline demo uses synthetic examples without calling an AI API.

## Features

- Text and screenshot analysis initiated by the user
- Risk categories: **Low**, **Moderate**, **Critical**, and **Uncertain**
- Explanation of potential scam tactics and psychological manipulation
- Plain-language safety recommendations, with English, Hindi (Devanagari), and Hinglish options
- Zero-shot and three-example few-shot prompt strategies for text
- Native Gemini screenshot analysis after image-size checks, orientation correction, and metadata removal
- Optional Groq text analysis and explicitly enabled Gemini-to-Groq **text** fallback
- Pydantic v2 response validation and inspectable structured JSON
- Labeled synthetic offline demonstrations
- India cybercrime reporting information: [cybercrime.gov.in](https://cybercrime.gov.in/) and national helpline **1930**

## Technology stack

- **Python** (project dependencies specify Python 3.11–3.13)
- **Streamlit** — web interface
- **Google `google-genai` SDK** — Gemini text and image analysis
- **Groq Python SDK** — optional text-only alternative
- **LangChain Core** (`ChatPromptTemplate`, `RunnableLambda`) — text prompt orchestration
- **Pydantic v2** — response schema validation
- **Pillow** — image preprocessing
- **python-dotenv** — local environment configuration
- **pytest** — automated tests

## Run locally on Windows

### 1. Requirements

Install Python 3.11, 3.12, or 3.13 and Git. Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/api-keys) if you want live text or screenshot analysis. A Groq API key is optional and only needed for Groq text analysis. The providers' availability, model IDs, rate limits, pricing, and account access may change.

### 2. Clone the repository

Open **Command Prompt (CMD)** or **PowerShell** and run:

```bat
git clone https://github.com/Dipankar-Maity/VeritasGuard.git
cd VeritasGuard
```

### 3. Create a virtual environment and install dependencies

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If you use another supported Python version, replace `-3.12` accordingly. You do **not** need a GPU.

### 4. Create your own local configuration

In **CMD**, run:

```bat
copy .env.example .env
notepad .env
```

In **PowerShell**, use `Copy-Item .env.example .env` instead of `copy` if preferred.

Edit the newly created `.env` file with **your own keys**:

```dotenv
GEMINI_API_KEY=YOUR_OWN_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.5-flash-lite

# Optional — Groq handles text only
GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-120b
```

- Replace `YOUR_OWN_GEMINI_API_KEY` with a key from your own Google AI Studio project.
- The example model `gemini-3.5-flash-lite` was used during development. If it is unavailable to your account, choose an available compatible Gemini model and update `GEMINI_MODEL` (or the app's model override).
- Leave `GROQ_API_KEY` empty unless you want to use Groq. If enabled, get your own key from [Groq Console](https://console.groq.com/keys) and confirm that `GROQ_MODEL` is available to your account.
- Each user is responsible for their own provider quotas, pricing, and API usage.
- **Never commit, share, or upload the populated `.env` file.** The repository's `.gitignore` excludes `.env` and `.venv/`. The committed `.env.example` contains placeholders only.

### 5. Start the app

```bat
.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local address shown in the terminal (normally **http://localhost:8501**).

Select **Text Message** or **Screenshot Image**, choose your language and (for text) provider/prompt strategy, then press **Analyze with VeritasGuard AI**. Screenshot analysis requires Gemini. The **Offline Demo** tab can be explored without an API key.

### 6. Run automated tests

```bat
.venv\Scripts\python.exe -m pytest -v -s
```

The developer's local test suite recorded **55 passing tests**. These tests are largely mocked/unit checks and do **not** establish real-world fraud-detection accuracy or guarantee that a live API will always respond. Results depend on the installed code, dependencies, and environment.

## How other people use their own API keys

Everyone who clones the GitHub repository creates **their own** `.env` file from `.env.example`. The application reads that local file when started; it does **not** use the original developer's private credentials. Groq is optional, and users should only enable it if they understand that their submitted text will be sent to that provider.

**GitHub source-code URL:** https://github.com/Dipankar-Maity/VeritasGuard  
This repository link is **not** a hosted public Streamlit application. To use the application, run it locally using the instructions above or deploy it separately with securely configured secrets.

## Privacy, security, and limitations

- Messages and uploaded images are **untrusted input**. VeritasGuard does not execute code or automatically follow links embedded in them.
- Live analysis sends the submitted text or screenshot to the selected cloud AI provider only after the user clicks **Analyze**. Screenshots are sent to Gemini, not Groq.
- **Image metadata removal is not visual redaction.** Crop or hide personal identifiers, OTPs, bank details, and other private information **before** uploading screenshots.
- AI-generated classifications may be incomplete or incorrect. Pydantic checks output **structure**, not factual truth, message authenticity, or external safety.
- The system does not conduct sender/domain reputation checks, QR payload decoding, payment execution, background interception, account verification, or live threat-intelligence lookups.
- An HTTP 503/504 or quota error indicates an unsuccessful API request, not a legitimate/safe classification. The text fallback to Groq must be explicitly enabled; there is no automatic image fallback.
- For suspected cybercrime in India, consult the official [National Cyber Crime Reporting Portal](https://cybercrime.gov.in/). If financial fraud has occurred, promptly contact your bank and the national helpline **1930**.

## Project structure

| File or directory | Purpose |
| --- | --- |
| `app.py` | Streamlit user interface, mode selection, and result display |
| `analyzer.py` | Gemini/Groq text analysis, prompt strategies, orchestration, and demo samples |
| `image_analyzer.py` | Image preprocessing and Gemini image analysis |
| `schema.py` | Pydantic v2 result schema |
| `taxonomy.py` | Project-defined fraud categories |
| `.env.example` | Safe environment-variable template; copy it to `.env` locally |
| `requirements.txt` | Python dependencies |
| `tests/` | Automated tests |
| `docs/` | Architecture, methodology, synopsis alignment, and testing instructions |

Further project documentation: [`docs/SYSTEM_ARCHITECTURE.md`](docs/SYSTEM_ARCHITECTURE.md), [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md), [`docs/SYNOPSIS_COMPLIANCE.md`](docs/SYNOPSIS_COMPLIANCE.md), [`docs/TESTING_GUIDE.md`](docs/TESTING_GUIDE.md), and [`WINDOWS_INTEGRATION.md`](WINDOWS_INTEGRATION.md).

## Academic context

VeritasGuard is a societal-impact academic prototype for the NVIDIA AI & Deep Learning RTD Open Elective at Dayananda Sagar University. It aims to make cyber-fraud warnings understandable to users of different language backgrounds; it does **not** replace professional cybersecurity investigation or official verification.
