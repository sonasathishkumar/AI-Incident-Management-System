import requests
import json

def triage_alert(alert_text):

    prompt = f"""
You are a DevOps incident triage AI.

Return ONLY valid JSON.
Do not explain.
Do not use markdown.

Format:
{{
  "severity": "",
  "component": "",
  "possible_causes": [],
  "suggested_actions": []
}}

Alert:
{alert_text}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        }
    )

    raw_output = response.json()["response"].strip()

    # Try direct parsing first
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        pass

    # Attempt to auto-fix incomplete JSON
    if not raw_output.endswith("}"):
        raw_output += "}"

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return {
            "error": "JSON parsing failed",
            "raw": raw_output
        }
