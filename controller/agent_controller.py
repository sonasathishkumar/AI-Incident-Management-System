from agents.triage_agent import triage_alert
from agents.remediation_agent import get_remediation_steps
from agents.postmortem_agent import generate_postmortem
from utils.logger import log_incident

# 🔥 Database imports
from database.database import SessionLocal
from database.models import Incident


class AgentController:

    # ===============================
    # Escalation Logic
    # ===============================
    def should_escalate(self, severity: str) -> bool:
        """
        Decide whether the incident should be escalated.
        """
        return severity.lower() in ["high", "critical"]


    # ===============================
    # Save to Database (JSON Version)
    # ===============================
    def save_to_database(
        self,
        alert_message: str,
        severity: str,
        triage_result: dict,
        remediation_steps: list,
        postmortem: str | None
    ):
        """
        Save incident into database using JSON columns.
        """
        db = SessionLocal()

        try:
            incident = Incident(
                alert_message=alert_message,
                severity=severity,
                component=triage_result.get("component", None),

                # 🔥 REAL JSON STORAGE (No str())
                triage=triage_result,
                remediation=remediation_steps,

                postmortem=postmortem
            )

            db.add(incident)
            db.commit()
            db.refresh(incident)

        finally:
            db.close()


    # ===============================
    # Main Incident Pipeline
    # ===============================
    def process_incident(self, alert_message: str) -> dict:
        """
        Main pipeline that processes an incident.
        """

        # 1️⃣ Triage Analysis
        triage_result = triage_alert(alert_message)

        # 2️⃣ Extract Component
        component = triage_result.get("component", "")

        # 3️⃣ Get Remediation Steps
        remediation_steps = get_remediation_steps(component)

        # 4️⃣ Determine Severity
        severity = triage_result.get("severity", "low")

        # 5️⃣ Prepare Response
        response = {
            "alert_message": alert_message,
            "severity": severity,
            "triage": triage_result,
            "remediation": remediation_steps,
            "escalated": False,
            "postmortem": None
        }

        postmortem = None

        # 6️⃣ Escalation Logic
        if self.should_escalate(severity):
            response["escalated"] = True

            postmortem = generate_postmortem(alert_message, triage_result)
            response["postmortem"] = postmortem

            log_incident(
                alert_message,
                triage_result,
                remediation_steps,
                postmortem=postmortem
            )
        else:
            log_incident(
                alert_message,
                triage_result,
                remediation_steps
            )

        # 7️⃣ Save to Database
        self.save_to_database(
            alert_message,
            severity,
            triage_result,
            remediation_steps,
            postmortem
        )

        return response
