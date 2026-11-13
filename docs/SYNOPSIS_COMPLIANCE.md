# Comparison with Submitted Synopsis — 11 November 2026

**Interpretation:** This checklist differentiates implemented source code from features verified live. The synopsis is a *proposal*; changed libraries/models are documented here rather than hidden.

| Submitted item | Status in code | Verification / honest scope |
|---|---|---|
| GenAI / LLM societal use case | IMPLEMENTED | Gemini text analysis previously demonstrated live. |
| Raw SMS/WhatsApp/Telegram/email text | IMPLEMENTED | User-pasted text, NOT automatic interception. |
| Multimodal screenshot ingestion | IMPLEMENTED | Gemini native image pathway; previous screenshot test succeeded live before final consolidation. |
| Image normalization / Pillow | IMPLEMENTED | Type/size/pixel, EXIF orientation and metadata stripping. |
| Native visual text understanding (without separate OCR) | IMPLEMENTED | Gemini SDK image bytes; independent OCR not installed. |
| QR-payment screenshots | PARTIAL | Contextual visible-image analysis, **no QR payload decoding or verification**. |
| Cognitive deceptive-tactic analysis | IMPLEMENTED | Model generates categories, tactics and triggers. |
| Zero-shot prompts | IMPLEMENTED | Selectable in UI. |
| Few-shot prompts | IMPLEMENTED | Three synthetic examples, selectable in UI. |
| LangChain prompt orchestration | IMPLEMENTED | `ChatPromptTemplate` and `RunnableLambda` sequence for text analysis; needs installed deps for live demonstration. |
| Gemini provider | IMPLEMENTED | Configurable via GEMINI_MODEL, default existing key. |
| Groq / Llama-3-70B fallback | PARTIAL / REPLACED | Optional text Groq integration using current `openai/gpt-oss-120b`; needs GROQ_API_KEY and a live test. Original model name retired. |
| Pydantic JSON enforcement | IMPLEMENTED | All API model outputs parsed into FraudAnalysisResult. Validation doesn't prove truth. |
| Low / Moderate / Critical risk | IMPLEMENTED | Plus Uncertain to avoid false safety claims. |
| `is_safe` boolean | INTENTIONALLY NOT IMPLEMENTED | Unsafe definitive safety assertion; replaced with risk plus uncertainty and disclaimer. |
| English / Hindi / vernacular | IMPLEMENTED, LIVE TEST PENDING | English previously live tested, Hindi sample present; Hinglish output option now wired for both modes. |
| Plain-language safety steps | IMPLEMENTED | English/Hindi/Hinglish requested, accuracy still requires caution. |
| National reporting portal and 1930 | IMPLEMENTED | Official portal link and helpline in UI. |
| Functional Streamlit dashboard | IMPLEMENTED | Previously launched and visually verified; consolidated version needs local launch check. |
| Offline demonstration | IMPLEMENTED | Clearly labeled fixed synthetic cases, not live model results. |
| Ready-to-deploy prototype | PARTIAL | Local Windows launch supported; public deployment not performed. |
| 100% guaranteed factual outputs / hallucination resistance | UNSUPPORTED CLAIM | No current LLM or JSON schema guarantees all results are factually correct. |

## Academic changes from the original proposal
- **Gemini 1.5 Flash → configurable modern Gemini model**, sample `.env.example` uses `gemini-3.8-flash` as used by the live prototype.
- **Groq Llama-3-70B → optional `openai/gpt-oss-120b` text model**; Groq API account and key needed for live verification.
- **LangChain** is now used for text prompt/runnable orchestration; Gemini image calls stay native.
- **"automatic interception"** is replaced with honest, explicit user-initiated submission.
- **"guaranteed factual JSON"** is replaced with Pydantic structure validation, source-grounded prompting and clear limitations.

Do not claim performance percentages or extensive field trials in the report unless you actually conduct them.
