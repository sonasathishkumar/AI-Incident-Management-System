from database.database import SessionLocal
from database.models import User
from auth.password_handler import hash_password

db = SessionLocal()

username = "admin"
password = "admin123"
role = "admin"

existing_user = db.query(User).filter(
    User.username == username
).first()

if existing_user:
    print("Admin already exists!")
else:
    new_user = User(
        username=username,
        hashed_password=hash_password(password),
        role=role
    )

    db.add(new_user)
    db.commit()

    print("✅ Admin created successfully!")