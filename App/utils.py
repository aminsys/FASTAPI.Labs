from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Hashing algorith we want to use

def hash(password: str):
    return pwd_context.hash(password)