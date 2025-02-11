from passlib.context import CryptContext

# using bcrypt to hash passwords
pwd_context = CryptContext(schemes=["bcrypt"])

def hash(str_passwor:str)->str:
    return pwd_context.hash(str_passwor)