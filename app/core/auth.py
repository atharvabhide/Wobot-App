from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from dotenv import load_dotenv

exists = load_dotenv()


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

if exists:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
else:
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """
    Hashes the password using bcrypt

    Args:
    password: str: The password to be hashed

    Returns:
    str: The hashed password
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """
    Verifies the password using bcrypt

    Args:
    password: str: The password to be verified
    hashed_pass: str: The hashed password to be verified against

    Returns:
    bool: True if the password is verified, False otherwise
    """
    return password_context.verify(password, hashed_pass)


def create_access_token(
    subject: Union[str, Any],
    expires_delta: int = None
) -> str:
    """
    Creates an access token using the subject
    and the expiration time

    Args:
    subject: Union[str, Any]: The subject of the token
    expires_delta: int: The expiration time of the token

    Returns:
    str: The encoded token
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: int = None
) -> str:
    """
    Creates a refresh token using the subject
    and the expiration time

    Args:
    subject: Union[str, Any]: The subject of the token
    expires_delta: int: The expiration time of the token

    Returns:
    str: The encoded token
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
