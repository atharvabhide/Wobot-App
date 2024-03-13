import uuid
from sqlalchemy import Column, String, DateTime, func
from db.config import Base
from pydantic import BaseModel


class Todo(Base):
    """
    Todo model

    Attributes
    ----------
    id : str
        Todo id
    title : str
        Todo title
    description : str
        Todo description
    user_email : str
        User email
    created_at : datetime
        Todo creation date
    updated_at : datetime
        Todo update date
    """

    __tablename__ = "todo"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        index=True,
    )
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    user_email = Column(String(255), index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.current_timestamp()
    )


class TodoCreateUpdate(BaseModel):
    """
    TodoCreateUpdate model

    Attributes
    ----------
    title : str
        Todo title
    description : str
        Todo description
    user_email : str
        User email
    """

    title: str
    description: str
