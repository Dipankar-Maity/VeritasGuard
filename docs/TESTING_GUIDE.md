# Testing and Evidence Guide

## Repeat on Windows (offline/mocked)
```powershell
cd "D:\Project\Open Elective Project\VeritasGuard"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v -s
```
Tests are mocked; **they should not contact Google or Groq**. Capture the full final pytest summary as authentic report evidence.

## One live integration check per provider
1. Start Streamlit with `.\.venv\Scripts\python.exe -m streamlit run app.py`.
2. Select **Text / English / Gemini / zero-shot**. Paste a synthetic fake-bank OTP request. Submit once, capture risk and JSON output.
3. Select **Screenshot / Gemini**. Use synthetic electricity-disconnection screenshot. Confirm preview and submit once, capture output.
4. Test a Hindi synthetic message and then Hinglish output. Capture actual output (no need to fabricate translation quality).
5. Optionally set GROQ_API_KEY in private `.env`, select **Groq** for **text**, submit a single synthetic message. Capture provider attribution if successful.
6. For a synthetic image with QR context, check whether it gives warnings without claiming it has decoded or verified the QR payload.
7. For ambiguous short messages, check whether it uses `Uncertain` where appropriate. Avoid assuming a particular category for every sample.
8. If API says 429/503/504, record the result and stop retries; the offline demo remains available.

## Security / privacy checks
- Confirm `.env` never appears under `git status --short`; never upload or include it in screenshots.
- Image metadata stripping does **not** remove personal information visible in pixels; use synthetic images or manually redact.
- Confirm no browser opening, code execution, auto-sending data, or quiet Groq image fallback occurs.
- Confirm error messages do not reveal API keys or model output bodies.

## Evaluation table template (fill using genuine observations)
| Case | Input | Expected warning signs | Actual risk | Observations | Pass/fail |
|---|---|---|---|---|---|
| Bank KYC request | Synthetic text | OTP, authority, urgency | *To test* | *To test* | *To test* |
| Electricity cutoff | Synthetic screenshot | urgency, UPI PIN | *To test* | *To test* | *To test* |
| QR refund lure | Synthetic screenshot | pay-to-receive claim | *To test* | *To test* | *To test* |
| Normal delivery message | Synthetic text | minimal evidence / caution | *To test* | *To test* | *To test* |
| Bare "hello" | Synthetic text | insufficient context | *To test* | *To test* | *To test* |

**Do not report accuracy, precision, recall or F1 without a labeled dataset and actual counted outcomes.**

## Earlier progress vs this package
- Earlier Milestone 2 on Windows: **30 tests passed** and one successful real Gemini screenshot analysis was shown in chat.
- Final consolidated package: run the expanded tests on **your Windows installation**; the Linux sandbox may not have the Google SDK, Groq, Streamlit or LangChain available. A mock-assisted sandbox result is **not** a real cloud integration result.
