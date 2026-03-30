import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def diagnose_and_fix(errors: list, attempt: int) -> dict:
    errors_text = "\n".join([f"- {e}" for e in errors])
    prompt = f"""You are a data engineering expert.
A data pipeline has failed with these errors (attempt {attempt}):
{errors_text}

For each error, provide a specific fix.
Reply in EXACTLY this format:
DIAGNOSIS: one sentence explaining root cause
FIX_1: specific fix for first error
FIX_2: specific fix for second error (if exists)
FIX_3: specific fix for third error (if exists)
CONFIDENCE: HIGH or MEDIUM or LOW"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return parse_fix(res.choices[0].message.content, errors)

def parse_fix(text: str, errors: list) -> dict:
    result = {
        "raw": text,
        "diagnosis": "",
        "fixes": [],
        "confidence": "LOW"
    }
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("DIAGNOSIS:"):
            result["diagnosis"] = line.split("DIAGNOSIS:", 1)[-1].strip()
        elif line.startswith("FIX_"):
            fix = line.split(":", 1)[-1].strip()
            if fix:
                result["fixes"].append(fix)
        elif line.startswith("CONFIDENCE:"):
            if "HIGH" in line: result["confidence"] = "HIGH"
            elif "MEDIUM" in line: result["confidence"] = "MEDIUM"
    if not result["fixes"]:
        result["fixes"] = [f"Fix: {e}" for e in errors]
    return result