from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


exists = load_dotenv()
if exists:
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_PORT = os.getenv("DB_PORT")
    DATABASE_URL = f"mysql+mysqlconnector:// \
        {DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = os.environ["DATABASE_URL"]
    print(DATABASE_URL, flush=True)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_tables():
    """
    Create tables in the database
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Create a new database session for each request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
