# Methodology — GenAI, LLMs and Scam Deconstruction

## Academic framing
VeritasGuard is an RTD societal-use-case implementation, not a trained-from-scratch fraud classifier. It uses pretrained Gemini multimodal LLM reasoning for text/vision and optional Groq-hosted text generation. No dedicated GPU is required to run the Streamlit client; model inference happens on provider infrastructure.

## Prompting and orchestration
**Zero-shot:** a role-and-safety system instruction requests explicit classification, threat cues, triggers, uncertainty and actions without synthetic demonstration examples.

**Few-shot:** the same instructions include **three small synthetic examples** of bank KYC, electricity disconnection, and Telegram task-job lures. Examples are *illustrations*, not evidence about a new message; outputs should not simply copy them.

**LangChain text pathway:** the `run_langchain_pipeline` function builds validated untrusted input, formats a `ChatPromptTemplate`, invokes the selected provider with `RunnableLambda` once, and parses JSON with Pydantic. A small wrapper preserves backwards-compatible `analyze_message` usage. **Vision** uses the native `google-genai` `types.Part.from_bytes` path instead of a text-only LangChain chat adapter.

**Cyber-fraud taxonomy:** `taxonomy.py` provides project-defined teaching categories: banking/KYC, UPI/payment, electricity, fake delivery, fake job/task, reward, authority impersonation, investment, malicious APK/remote access, QR-payment, potentially legitimate, unknown, etc. It is **not a formal official governmental taxonomy**. Each assessment must be grounded in visible cues; a URL/QR/phone number is never confirmed without separate lookup (not implemented).

## Risk and uncertainty
- `Critical`: several severe warning signs such as urgent credential/UPI PIN requests or coercive payment instructions.
- `Moderate`: concerning offers/contacts with incomplete evidence.
- `Low`: few observed warning signs in the available information, never a verified-safe guarantee.
- `Uncertain`: insufficient/unreadable/context-limited information.

The AI may generate `observed_evidence`, `unverified_assumptions`, `uncertainty_explanation`, and `model_provider`. Pydantic validates type/schema and prevents malformed dashboard displays; it **cannot stop hallucinations or prove the classification is correct**.

## Accessibility and societal value
English, Hindi, and Hinglish output options support citizens with varied digital literacy. Steps advise independently checking institutions and, in relevant cases, reporting to https://cybercrime.gov.in/ or calling 1930 quickly for cyber financial fraud.

## Testing and evaluation
Unit tests use provider mocks (no real API charges) to check the code path. A successful local demo with user-supplied synthetic messages/screenshots is separate evidence of live functionality. No real-world accuracy percentage, false-positive rate, recall or population-level effectiveness is claimed unless a documented labeled evaluation is performed.

## References / API documentation
- [Google Gen AI Python SDK](https://googleapis.github.io/python-genai/)
- [Groq API reference](https://console.groq.com/docs/api-reference)
- [LangChain core runnables](https://reference.langchain.com/python/langchain-core/runnables)
- [National Cyber Crime Reporting Portal](https://cybercrime.gov.in/)
