from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter
)
from sqlalchemy.orm import Session
from db.user_repository import create_user
from models.users import (
    User,
    UserCreateUpdate,
    TokenSchema
)
from core.auth import (
    create_access_token,
    create_refresh_token,
    verify_password
)
from fastapi.security import OAuth2PasswordRequestForm
from core.deps import get_current_user
from db.config import get_db


userRouter = APIRouter()


@userRouter.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    tags=["Users"]
)
async def create_user_api(
    data: UserCreateUpdate,
    db: Session = Depends(get_db)
):
    """
    Create a new user

    Args:
    data (UserCreateUpdate): The user data
    db (Session): The database session. Defaults to Depends(get_db).

    Returns:
    db_user: The created user
    """
    if "@" not in data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email"
        )
    user = db.query(User).filter(User.email == data.email).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )
    db_user = User(**data.dict())
    db_user = create_user(db, db_user)
    return db_user


@userRouter.post(
    "/login",
    response_model=TokenSchema,
    tags=["Users"]
)
async def login_user_api(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login a user

    Args:
    form_data (OAuth2PasswordRequestForm): The user login data
    db (Session): The database session. Defaults to Depends(get_db).

    Returns:
    dict: The user access and refresh tokens
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    hashed_pass = user.hashed_password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


@userRouter.get(
    "/users/me",
    tags=["Users"]
)
async def get_me(user: User = Depends(get_current_user)):
    """
    Get the current user

    Args:
    user (User): The user object. Defaults to Depends(get_current_user).

    Returns:
    user: The user object
    """
    return user
