from database.database import SessionLocal
from database.models import User
from auth.password_handler import hash_password

db = SessionLocal()

username = "analyst"
password = "analyst123"

existing = db.query(User).filter(User.username == username).first()

if existing:
    print("User already exists!")
else:
    user = User(
        username=username,
        hashed_password=hash_password(password),
        role="user"
    )

    db.add(user)
    db.commit()
    print("Analyst created successfully!")

db.close()