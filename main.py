from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, SQLModel, create_engine, select
from models import User, Book, Exchange, Rating, create_db_and_tables
from crud import create_user, get_user_by_id, create_book, get_books, create_exchange, get_exchanges, create_rating, get_ratings_for_user
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Создаем базу данных и таблицы
create_db_and_tables()

# Подключение к базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Маршрут для главной страницы
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Маршрут для регистрации пользователя
@app.post("/register")
async def register(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    address: str = Form(None)
):
    user = User(first_name=first_name, last_name=last_name, email=email, password=password, address=address)
    created_user = create_user(user)
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

# Маршрут для входа пользователя
@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = get_user_by_email(email)
    if not user or user.password!= password:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid credentials"})
    response = RedirectResponse(url=f"/profile/{user.id}", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user_id", value=user.id)
    return response

# Маршрут для просмотра профиля пользователя
@app.get("/profile/{user_id}", response_class=HTMLResponse)
async def view_profile(request: Request, user_id: int):
    user = get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

# Маршрут для отображения доступных книг
@app.get("/books", response_class=HTMLResponse)
async def list_books(request: Request):
    books = get_books()
    return templates.TemplateResponse("books.html", {"request": request, "books": books})

# Маршрут для формы добавления книги
@app.get("/books/add", response_class=HTMLResponse)
async def add_book_form(request: Request):
    return templates.TemplateResponse("add_book.html", {"request": request})

# Маршрут для добавления книги
@app.post("/books/add")
async def add_book(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    year: int = Form(...),
    condition: str = Form(...),
    owner_id: int = Form(...)
):
    book = Book(title=title, author=author, genre=genre, year=year, condition=condition, owner_id=owner_id)
    created_book = create_book(book)
    return RedirectResponse(url="/books", status_code=status.HTTP_303_SEE_OTHER)

# Маршрут для отображения списка обменов книгами
@app.get("/exchanges", response_class=HTMLResponse)
async def list_exchanges(request: Request):
    exchanges = get_exchanges()
    return templates.TemplateResponse("exchanges.html", {"request": request, "exchanges": exchanges})

# Маршрут для отправки запроса на обмен книгами
@app.post("/exchanges/request")
async def request_exchange(
    book_to_send_id: int = Form(...),
    book_to_receive_id: int = Form(...),
    requester_id: int = Form(...),
    responder_id: int = Form(...)
):
    exchange = Exchange(
        book_to_send_id=book_to_send_id,
        book_to_receive_id=book_to_receive_id,
        requester_id=requester_id,
        responder_id=responder_id
    )
    created_exchange = create_exchange(exchange)
    return RedirectResponse(url="/exchanges", status_code=status.HTTP_303_SEE_OTHER)

# Маршрут для страницы входа
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Маршрут для страницы регистрации
@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
