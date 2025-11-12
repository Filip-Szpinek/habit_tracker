from fastapi import APIRouter, Request, Form, Depends, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import SessionLocal
from models import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

#funkcja do pobierania DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#sprawdzanie, czy użytkownik jest zalogowany
def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if not user_id:
        raise HTTPException(status_code=401, detail="Niezalogowany")
    if not user:
        raise HTTPException(status_code=401, detail="Niezalogowany")
    return user

#zwraca stronne do logowania
@router.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
        "request": request
        }
    )

#funkcja do logowania
@router.post("/login")
def login(request: Request, response: Response, login: str = Form(...),password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(and_(User.login == login, User.password == password)).first()
    if user:
        response = RedirectResponse(url="/habit-tracker", status_code = 303)
        response.set_cookie(key="user_id", value=str(user.user_id)) #dodawanie cookie 
        return response
    else:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "message": "Błędne hasło"
            }
        )

#chronione trasa
@router.get("/habit-tracker", response_class=HTMLResponse)
def habit_tracker(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "habit_tracker.html",
        {
            "request": request,
            "user_id": current_user.user_id,
            "login": current_user.login,
            "password": current_user.password
        }
    )

#wylogowanie
@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="user_id")
    return response
