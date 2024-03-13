from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.auth import ALGORITHM, JWT_SECRET_KEY

from jose import jwt
from pydantic import ValidationError
from models.users import TokenPayload, User
from db.config import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


def get_db():
    """
    Create a new database session for each request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(reuseable_oauth),
    db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.execute(
        text(f"SELECT * FROM user WHERE email = '{token_data.sub}'")
    ).fetchone()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    data = {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "created_at": user[5],
        "updated_at": user[6],
    }

    return User(**data)
