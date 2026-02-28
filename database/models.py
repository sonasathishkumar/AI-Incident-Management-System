from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    JSON,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base


# ===============================
# USER MODEL
# ===============================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password = Column(String, nullable=False)

    role = Column(String, default="user")   # admin / user
    is_active = Column(Boolean, default=True)

    # Relationship
    incidents = relationship(
        "Incident",
        back_populates="owner"
    )


# ===============================
# INCIDENT MODEL
# ===============================
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    alert_message = Column(Text, nullable=False)
    severity = Column(String, nullable=False)
    component = Column(String)

    # AI Outputs
    triage = Column(JSON)
    remediation = Column(JSON)

    postmortem = Column(Text)

    # ✅ INCIDENT LIFECYCLE
    status = Column(String, default="OPEN")
    # OPEN → IN_PROGRESS → RESOLVED → CLOSED

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # OWNER
    assigned_to = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="incidents"
    )