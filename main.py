from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import SessionLocal, engine
from models import Base, User

Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
def login(request: Request, login: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(and_(User.login == login, User.password == password)).first()
    if user:
        return templates.TemplateResponse("habit_tracker.html", {"request": request, "login": login, "password": password, "user_id": user.user_id})
    else:
        return templates.TemplateResponse("index.html", {"request": request, "message": "Błędne hasło"})
