from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.todo_repository import (
    create_todo,
    get_todo_by_id,
    get_todos,
    update_todo,
    delete_todo,
)
from models.todos import TodoCreateUpdate
from core.deps import get_current_user
from db.config import get_db
from models.users import User


todoRouter = APIRouter()


@todoRouter.post("/todos", status_code=status.HTTP_201_CREATED, tags=["Todos"])
async def create_todo_api(
    data: TodoCreateUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        todo = create_todo(db, data, user)
        return todo
    except Exception as e:
        raise e


@todoRouter.get("/todos", tags=["Todos"])
async def get_todos_api(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        todos = get_todos(db, user)
        if todos == "Unauthorized":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        if todos == "Not Found":
            return []
        return todos
    except Exception as e:
        raise e


@todoRouter.get("/todos/{todo_id}", tags=["Todos"])
async def get_todo_api(
    todo_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        todo = get_todo_by_id(db, todo_id, user)
        if todo == "Unauthorized":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        if todo == "Not Found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
            )
        return todo
    except Exception as e:
        raise e


@todoRouter.put("/todos/{todo_id}", tags=["Todos"])
async def update_todo_api(
    todo_id: str,
    data: TodoCreateUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        todo = update_todo(db, todo_id, data, user)
        if todo == "Unauthorized":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        if todo == "Not Found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
            )
        return todo
    except Exception as e:
        raise e


@todoRouter.delete(
    "/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todos"]
)
async def delete_todo_api(
    todo_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        response = delete_todo(db, todo_id, user)
        if response == "Unauthorized":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        if response == "Not Found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
            )
        return None
    except Exception as e:
        raise e
