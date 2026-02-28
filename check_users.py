from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ============================
# Database Dependency
# ============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================
# Create User
# ============================
@router.post("/")
def create_user(username: str, role: str, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.username == username
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=username,
        role=role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "role": new_user.role
    }


# ============================
# Get All Users
# ============================
@router.get("/")
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
        for user in users
    ]