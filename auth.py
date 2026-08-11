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

