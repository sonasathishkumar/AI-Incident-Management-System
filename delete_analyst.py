from database.database import SessionLocal
from database.models import User

db = SessionLocal()

user = db.query(User).filter(User.username == "analyst").first()

if user:
    db.delete(user)
    db.commit()
    print("Analyst deleted successfully")
else:
    print("Analyst not found")

db.close()
