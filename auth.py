import hashlib
import os
 
from sqlalchemy.orm import Session
from models import User

def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, hashed = stored_hash.split("$")
    except ValueError:
        return False
 
    check_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return check_hash == hashed

class AuthError(Exception):
    pass
 
 
def register_user(session: Session, username: str, password: str) -> User:

    username = username.strip()
 
    if not username or not password:
        raise AuthError("Username and password cannot be empty.")
 
    if len(password) < 4:
        raise AuthError("Password must be at least 4 characters.")
 
    existing = session.query(User).filter_by(username=username).first()
    if existing:
        raise AuthError(f"Username '{username}' is already taken.")
 
    user = User(username=username, password_hash=hash_password(password))
    session.add(user)
    session.commit()
    return user