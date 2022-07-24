from email_validator import validate_email, EmailNotValidError
from passlib.context import CryptContext


def check_email(email: str):
    try:

        return validate_email(email)
    except EmailNotValidError as e:
        return None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
