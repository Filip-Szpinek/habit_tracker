from database import SessionLocal
from models import User
from utils import hash_password

db = SessionLocal()
users = db.query(User).all()

for user in users:
    if user.password:
        # Zamiana starego hasła na hash sha256_crypt
        user.password = hash_password(user.password)

db.commit()
db.close()
print("Hasła zostały przekonwertowane na hash (sha256_crypt)")
