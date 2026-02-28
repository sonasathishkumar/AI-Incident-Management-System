import json

def normalize(text):
    return text.lower().replace("_", " ").strip()

def get_remediation_steps(component):

    with open("data/runbooks.json", "r") as f:
        runbooks = json.load(f)

    normalized_component = normalize(component)

    for runbook in runbooks:
        runbook_component = normalize(runbook["component"])

        # Flexible keyword match
        if runbook_component in normalized_component or normalized_component in runbook_component:
            return runbook["steps"]

    return ["No matching runbook found. Manual investigation required."]
