from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from db.config import create_tables
from routers.users import userRouter
from routers.todos import todoRouter


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRouter)
app.include_router(todoRouter)


@app.get("/", status_code=status.HTTP_200_OK, tags=["Root"])
def root():
    """
    Root route

    Returns:
    dict: The message
    """
    return {"message": "Wobot ToDo App with User Auth"}


@app.on_event("startup")
def on_startup():
    """
    Create the tables on startup
    """
    create_tables()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
