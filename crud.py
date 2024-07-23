from models import User, Book, Exchange, Rating, engine
from sqlmodel import Session, select

def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def get_user_by_email(email: str):
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

def create_book(book: Book):
    with Session(engine) as session:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

def get_books():
    with Session(engine) as session:
        statement = select(Book)
        return session.exec(statement).all()

def create_exchange(exchange: Exchange):
    with Session(engine) as session:
        session.add(exchange)
        session.commit()
        session.refresh(exchange)
        return exchange

def get_exchanges():
    with Session(engine) as session:
        statement = select(Exchange)
        return session.exec(statement).all()

def create_rating(rating: Rating):
    with Session(engine) as session:
        session.add(rating)
        session.commit()
        session.refresh(rating)
        return rating

def get_ratings_for_user(user_id: int):
    with Session(engine) as session:
        statement = select(Rating).where(Rating.user_id == user_id)
        return session.exec(statement).all()