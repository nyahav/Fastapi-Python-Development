from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def hash(oassword: str):
    return pwd_context.hash(oassword)