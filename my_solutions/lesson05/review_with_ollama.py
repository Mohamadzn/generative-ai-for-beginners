# review_with_ollama.py
# Lesson 05 - Advanced Prompt Engineering with Ollama (robust output parsing)
# Works even if the model does NOT return JSON and instead returns a code block.

from __future__ import annotations

import base64
import json
import re
from pathlib import Path

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "phi3:mini"  # ✅ lightweight model

ORIGINAL_FILE = Path("original_app.py")
OUTPUT_FILE = Path("improved_app.py")


def call_ollama(messages):
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.2},
        },
        timeout=600,
    )
    r.raise_for_status()
    return r.json()["message"]["content"]


def extract_code_block(text: str) -> str | None:
    """
    Extract python code from ```python ... ``` or ``` ... ``` blocks.
    Returns None if no code block found.
    """
    # Prefer ```python ... ```
    m = re.search(r"```python\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # Fallback: any ``` ... ```
    m = re.search(r"```\s*(.*?)```", text, flags=re.DOTALL)
    if m:
        return m.group(1).strip()

    return None


def main():
    if not ORIGINAL_FILE.exists():
        print("❌ original_app.py not found in this folder.")
        print("Create original_app.py first.")
        return

    code = ORIGINAL_FILE.read_text(encoding="utf-8")

    # Keep prompt short for phi3:mini, but still clear
    system = """
You are a senior Python engineer.
Return ONLY ONE of the following:
A) STRICT JSON with keys: issues (list), improved_code_b64 (string)
or
B) A single Python code block (```python ... ```)

No extra explanations.
""".strip()

    user = f"""
Improve this Flask app:
- Use jsonify for responses
- Validate the 'name' parameter (non-empty string)
- Add basic try/except
- Keep it small and runnable

CODE:
{code}
""".strip()

    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]

    print("⏳ Calling Ollama (phi3:mini)...")
    out = call_ollama(messages)

    # 1) Try JSON path first
    try:
        data = json.loads(out)
        issues = data.get("issues", [])
        b64 = data.get("improved_code_b64", "")

        if isinstance(issues, list) and isinstance(b64, str) and b64.strip():
            improved_code = base64.b64decode(b64).decode("utf-8", errors="strict")
            OUTPUT_FILE.write_text(improved_code, encoding="utf-8")

            print("\n✅ Issues found:")
            for i, issue in enumerate(issues, 1):
                print(f"{i}. {issue}")

            print(f"\n✅ Saved improved code to: {OUTPUT_FILE.resolve()}")
            return
    except Exception:
        pass

    # 2) Fallback: extract code block
    extracted = extract_code_block(out)
    if extracted:
        OUTPUT_FILE.write_text(extracted, encoding="utf-8")
        print(f"\n✅ Model returned a code block (not JSON). Saved to: {OUTPUT_FILE.resolve()}")
        print("\nNext:")
        print("  python improved_app.py")
        print("  open: http://127.0.0.1:5000/?name=Mohammad")
        return

    # 3) If neither worked, show raw output
    print("❌ Could not parse JSON or find a code block.")
    print("RAW OUTPUT:\n", out)


if __name__ == "__main__":
    main()