import requests

def generate_postmortem(alert_message, triage_result):

    prompt = f"""
You are a DevOps incident analysis AI.

Generate a professional postmortem report.

Include:
- Incident Summary
- Root Cause
- Actions Taken
- Prevention Recommendations

Alert:
{alert_message}

Triage Data:
{triage_result}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2
            }
        }
    )

    return response.json()["response"]
