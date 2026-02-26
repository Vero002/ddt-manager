from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

db = SessionLocal()

admin = User(
    username="admin",
    hashed_password=get_password_hash("admin123")
)

db.add(admin)
db.commit()
db.close()

print("Admin creato!")