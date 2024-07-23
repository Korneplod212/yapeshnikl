from sqlmodel import Field, SQLModel, create_engine, Session, select
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(unique=True)
    password: str
    address: Optional[str] = None

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    genre: str
    year: int
    condition: str
    rating: Optional[float] = None
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")

class Exchange(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_to_send_id: int = Field(foreign_key="book.id")
    book_to_receive_id: int = Field(foreign_key="book.id")
    status: str = "pending"
    requester_id: int = Field(foreign_key="user.id")
    responder_id: int = Field(foreign_key="user.id")

class Rating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    rating: int
    comment: Optional[str] = None

DATABASE_URL = "sqlite:///./knigi.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)