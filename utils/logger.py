import json
from datetime import datetime

def log_incident(alert, triage_result, remediation_steps, severity="low", postmortem=None):

    incident_record = {
        "timestamp": datetime.utcnow().isoformat(),
        "alert": alert,
        "severity": severity,
        "triage": triage_result,
        "remediation": remediation_steps,
        "postmortem": postmortem
    }

    with open("incident_log.json", "a") as f:
        f.write(json.dumps(incident_record) + "\n")
