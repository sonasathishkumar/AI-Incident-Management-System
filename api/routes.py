from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import timedelta

from controller.agent_controller import AgentController
from database.database import get_db
from database.models import Incident, User

from schemas.incident_schema import (
    IncidentResponse,
    IncidentUpdate
)
from schemas.assignment_schema import AssignIncident
from schemas.status_enum import IncidentStatus

from auth.auth_handler import create_access_token, verify_token
from auth.password_handler import verify_password


router = APIRouter()
controller = AgentController()


# =====================================================
# ✅ ADMIN CHECK
# =====================================================
def require_admin(token_data: dict = Depends(verify_token)):
    if token_data.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    return token_data


# =====================================================
# ✅ OWNER OR ADMIN CHECK
# =====================================================
def require_owner_or_admin(
    incident_id: int,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):

    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(404, "Incident not found")

    # Admin → full access
    if token_data["role"] == "admin":
        return incident

    user = db.query(User).filter(
        User.username == token_data["sub"]
    ).first()

    if incident.assigned_to != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this incident"
        )

    return incident


# =====================================================
# REQUEST MODEL
# =====================================================
class IncidentRequest(BaseModel):
    message: str


# =====================================================
# ✅ LOGIN
# =====================================================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        data={
            "sub": user.username,
            "role": user.role
        },
        expires_delta=timedelta(minutes=60)
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =====================================================
# ✅ CREATE INCIDENT
# =====================================================
@router.post(
    "/incident",
    response_model=IncidentResponse,
    status_code=201
)
def process_incident(
    request: IncidentRequest,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):

    result = controller.process_incident(request.message)

    user = db.query(User).filter(
        User.username == token_data["sub"]
    ).first()

    incident = Incident(
        alert_message=result["alert_message"],
        severity=result["severity"],
        component=result["triage"].get("component"),
        triage=result["triage"],
        remediation=result["remediation"],
        postmortem=result["postmortem"],
        status=IncidentStatus.OPEN,
        assigned_to=user.id
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


# =====================================================
# ✅ GET INCIDENTS
# =====================================================
@router.get(
    "/incidents",
    response_model=List[IncidentResponse]
)
def get_all_incidents(
    token_data: dict = Depends(verify_token),
    skip: int = Query(0),
    limit: int = Query(10),
    severity: Optional[str] = None,
    sort: str = "asc",
    db: Session = Depends(get_db),
):

    query = db.query(Incident)

    # Normal user → only assigned incidents
    if token_data["role"] != "admin":
        user = db.query(User).filter(
            User.username == token_data["sub"]
        ).first()

        query = query.filter(
            Incident.assigned_to == user.id
        )

    if severity:
        query = query.filter(
            Incident.severity == severity.upper()
        )

    if sort == "desc":
        query = query.order_by(
            Incident.created_at.desc()
        )
    else:
        query = query.order_by(
            Incident.created_at.asc()
        )

    return query.offset(skip).limit(limit).all()


# =====================================================
# ✅ GET SINGLE INCIDENT
# =====================================================
@router.get(
    "/incidents/{incident_id}",
    response_model=IncidentResponse
)
def get_incident(
    incident: Incident = Depends(require_owner_or_admin)
):
    return incident


# =====================================================
# ✅ ASSIGN INCIDENT (ADMIN ONLY)
# =====================================================
@router.put("/incidents/{incident_id}/assign")
def assign_incident(
    incident_id: int,
    assignment: AssignIncident,
    token_data: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):

    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    user = db.query(User).filter(
        User.id == assignment.user_id
    ).first()

    if not incident or not user:
        raise HTTPException(404, "Not found")

    incident.assigned_to = user.id
    db.commit()

    return {"message": f"Assigned to {user.username}"}


# =====================================================
# ✅ UPDATE INCIDENT + STATUS WORKFLOW
# =====================================================
@router.put(
    "/incidents/{incident_id}",
    response_model=IncidentResponse
)
def update_incident(
    incident_update: IncidentUpdate,
    incident: Incident = Depends(require_owner_or_admin),
    db: Session = Depends(get_db),
):

    allowed_flow = {
        IncidentStatus.OPEN: [IncidentStatus.IN_PROGRESS],
        IncidentStatus.IN_PROGRESS: [IncidentStatus.RESOLVED],
        IncidentStatus.RESOLVED: [IncidentStatus.CLOSED],
        IncidentStatus.CLOSED: []
    }

    update_data = incident_update.model_dump(exclude_unset=True)

    # ✅ Validate status transition
    if "status" in update_data:
        new_status = update_data["status"]

        if new_status not in allowed_flow[incident.status]:
            raise HTTPException(
                400,
                f"Invalid status transition "
                f"{incident.status} → {new_status}"
            )

    for key, value in update_data.items():
        setattr(incident, key, value)

    db.commit()
    db.refresh(incident)

    return incident


# =====================================================
# ✅ DELETE INCIDENT
# =====================================================
@router.delete("/incidents/{incident_id}")
def delete_incident(
    incident: Incident = Depends(require_owner_or_admin),
    db: Session = Depends(get_db),
):

    db.delete(incident)
    db.commit()

    return {"message": "Incident deleted successfully"}

# =====================================================
# ✅ CREATE USER (ADMIN ONLY)
# =====================================================
class UserCreate(BaseModel):
    username: str
    password: str
    role: str


@router.post("/users")
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):

    existing_user = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    from auth.password_handler import hash_password

    new_user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "role": new_user.role
    }


# =====================================================
# ✅ GET ALL USERS
# =====================================================
@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
        for user in users
    ]