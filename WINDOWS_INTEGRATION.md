# VeritasGuard — Safely apply this ZIP to your working project

1. **Keep your existing Milestone 2 Git commit** (`8fda583`) on `main` as a recovery point. Use the feature branch `feature/final-synopsis-alignment` if it exists. Do not delete `.git`.
2. Stop the running Streamlit server with **Ctrl+C** in its terminal.
3. Make a backup folder or use your Git commit before replacing files.
4. Extract the ZIP **contents (files at ZIP root)** directly into `D:\Project\Open Elective Project\VeritasGuard` and accept replacing source files. The ZIP intentionally contains **no `.env`**, `.venv`, `.git`, or API keys; keep your local `.env`.
5. In PowerShell from that folder:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v -s
.\.venv\Scripts\python.exe -m streamlit run app.py
```
6. Verify text and screenshot analysis, Hindi/Hinglish and prompt strategy options, JSON display and offline demo.
7. **Optional Groq**: independently create a Groq API key, add `GROQ_API_KEY=...` privately in `.env`, then choose Groq for **text only**. Avoid doing this until the Gemini workflow is stable.
8. Once verified, inspect `git status --short`, review staged changes for secrets, and commit the feature branch. Do not publish private API keys or data.

If tests fail on Windows, capture only the exception summary and tests that failed, without showing `.env` values. Return the updated source ZIP to ChatGPT for targeted fixes.
