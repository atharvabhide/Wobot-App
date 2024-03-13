from sqlalchemy.orm import Session
from models.todos import Todo
from core.deps import get_current_user
from fastapi import Depends
from models.users import User


def create_todo(
    db: Session,
    data: Todo,
    user: User = Depends(get_current_user)
):
    """
    Create a new Todo

    Parameters
    ----------
    todo : Todo
        Todo data
    db: Session
        Database session
    user: User
        User data

    Returns
    -------
    Todo
        The created todo
    """
    try:
        todo = Todo(
            title=data.title,
            description=data.description,
            user_email=user.email
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "user_email": todo.user_email,
            "created_at": todo.created_at,
            "updated_at": todo.updated_at,
        }
    except Exception as e:
        raise e


def get_todo_by_id(
    db: Session,
    todo_id: str,
    user: User = Depends(get_current_user)
):
    """
    Read a Todo

    Parameters
    ----------
    todo_id : str
        Todo id
    db: Session
        Database session
    user: User
        User data

    Returns
    -------
    Todo
        The todo
    """
    try:
        todo = db.query(Todo).filter(Todo.id == str(todo_id)).first()
        if todo is None:
            return "Not Found"
        if todo.user_email != user.email:
            return "Unauthorized"
        return {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "user_email": todo.user_email,
            "created_at": todo.created_at,
            "updated_at": todo.updated_at,
        }
    except Exception as e:
        raise e


def get_todos(
    db: Session,
    user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
):
    """
    Read a list of Todos

    Parameters
    ----------
    skip : int, optional
        Skip the first n todos, by default 0
    limit : int, optional
        Limit the number of todos, by default 10
    db: Session
        Database session
    user: User
        User data

    Returns
    -------
    [Todo]
        List of todos
    """
    try:
        todos = (
            db.query(Todo)
            .filter(Todo.user_email == user.email)
            .offset(skip)
            .limit(limit)
            .all()
        )
        if len(todos) == 0:
            return "Not Found"
        for todo in todos:
            if todo.user_email != user.email:
                return "Unauthorized"
        return [
            {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "user_email": todo.user_email,
                "created_at": todo.created_at,
                "updated_at": todo.updated_at,
            }
            for todo in todos
        ]
    except Exception as e:
        raise e


def update_todo(
    db: Session,
    todo_id: str,
    todo: Todo,
    user: User = Depends(get_current_user)
):
    """
    Update a Todo

    Parameters
    ----------
    todo_id : str
        Todo id
    todo : Todo
        Todo data
    db: Session
        Database session
    user: User
        User data

    Returns
    -------
    Todo
        The updated todo
    """
    try:
        db_todo = db.query(Todo).filter(Todo.id == str(todo_id)).first()
        if db_todo is None:
            return "Not Found"
        if db_todo.user_email != user.email:
            return "Unauthorized"
        db_todo.title = todo.title
        db_todo.description = todo.description
        db.commit()
        db.refresh(db_todo)
        return {
            "id": db_todo.id,
            "title": db_todo.title,
            "description": db_todo.description,
            "user_email": db_todo.user_email,
            "created_at": db_todo.created_at,
            "updated_at": db_todo.updated_at,
        }
    except Exception as e:
        raise e


def delete_todo(
    db: Session,
    todo_id: str,
    user: User = Depends(get_current_user)
):
    """
    Delete a Todo

    Parameters
    ----------
    todo_id : str
        Todo id
    db: Session
        Database session
    user: User
        User data
    """
    try:
        todo = db.query(Todo).filter(Todo.id == str(todo_id)).first()
        if todo is None:
            return "Not Found"
        if todo.user_email != user.email:
            return "Unauthorized"
        db.delete(todo)
        db.commit()
    except Exception as e:
        raise e
