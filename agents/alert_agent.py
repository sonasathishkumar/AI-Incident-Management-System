import json

def load_alert():
    with open("data/sample_alerts.json", "r") as f:
        alerts = json.load(f)
    return alerts[0]
