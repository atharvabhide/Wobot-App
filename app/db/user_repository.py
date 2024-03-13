from sqlalchemy.orm import Session
from models.users import User
from core.auth import get_hashed_password


def create_user(
    db: Session,
    user: User
):
    """
    Create a new User

    Parameters
    ----------
    user : user
        User data
    db: Session
        Database session

    Returns
    -------
    User
        The created user
    """
    try:
        user.hashed_password = get_hashed_password(user.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
    except Exception as e:
        raise e
