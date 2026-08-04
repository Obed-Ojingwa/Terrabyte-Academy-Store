from app.core.security import get_password_hash

password = "securepassword123"
print(f"Hashing password: {password}")
hashed = get_password_hash(password)
print(f"Hashed: {hashed}")