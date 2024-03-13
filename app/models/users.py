import uuid
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.schema import UniqueConstraint
from db.config import Base
from pydantic import BaseModel


class User(Base):
    """
    User model

    Attributes
    ----------
    id : str
        User id
    name : str
        User name
    email : str
        User email
    _password : str
        User password
    hashed_password : str
        User hashed password
    created_at : datetime
        User creation date
    updated_at : datetime
        User update date
    """

    __tablename__ = "user"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        index=True,
    )
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column("password", String(255))
    hashed_password = Column(String(256))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.current_timestamp()
    )

    __table_args__ = (UniqueConstraint("email"),)


class UserCreateUpdate(BaseModel):
    """
    UserCreateUpdate model

    Attributes
    ----------
    name : str
        User name
    email : str
        User email
    password : str
        User password
    """

    name: str
    email: str
    password: str


class TokenSchema(BaseModel):
    """
    TokenSchema model

    Attributes
    ----------
    access_token : str
        User access token
    refresh_token : str
        User refresh token
    """

    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    """
    TokenPayload model

    Attributes
    ----------
    sub : str
        User email
    exp : int
        Token expiration time
    """

    sub: str = None
    exp: int = None
