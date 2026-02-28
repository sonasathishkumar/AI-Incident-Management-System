from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List
from schemas.status_enum import IncidentStatus


# ===============================
# RESPONSE MODEL
# ===============================
class IncidentResponse(BaseModel):
    id: int
    alert_message: str
    severity: str
    component: Optional[str]

    triage: Optional[Dict[str, Any]]
    remediation: Optional[List[Any]]

    postmortem: Optional[str]

    # ✅ ENUM STATUS
    status: IncidentStatus

    created_at: datetime

    class Config:
        from_attributes = True


# ===============================
# UPDATE MODEL
# ===============================
class IncidentUpdate(BaseModel):
    severity: Optional[str] = None
    component: Optional[str] = None

    triage: Optional[Dict[str, Any]] = None
    remediation: Optional[List[Any]] = None

    postmortem: Optional[str] = None

    # ✅ Controlled workflow status
    status: Optional[IncidentStatus] = None