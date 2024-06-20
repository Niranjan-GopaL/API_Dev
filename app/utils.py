# hashing passowrd
from passlib.context import CryptContext

# How we wanna encrypt the password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# simple steps to hash password
def hash_from_util(password : str):
    hashed_passwrd = pwd_context.hash(password)
    return hashed_passwrd
