from app import app, db
from models import User

with app.app_context():
    users = User.query.all()
    print(f"\nTotal users: {len(users)}\n")
    for u in users:
        print(f"Email: {u.email}")
        print(f"Role: {u.role}")
        print(f"Has password: {u.password_hash is not None}")
        print("-" * 40)
