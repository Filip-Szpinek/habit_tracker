from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import LoginForm
from utils import verify_password, hash_password, create_access_token, verify_access_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")

#funkcja do pobierania DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#strona główna
@router.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#login
@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    #walidacja Pydantic
    try:
        form_data = LoginForm(login=login, password=password)
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": f"Błędne dane: {e}"},
            status_code=400
        )

    user = db.query(User).filter(User.login == form_data.login).first()

    if not user:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "Nie ma takiego użytkownika"},
            status_code=404
        )
    if not verify_password(form_data.password, user.password):
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "Błędne hasło"},
            status_code=403
        )

    #generowanie tokena JWT
    token = create_access_token({"id": user.user_id, "sub": user.login})

    response = RedirectResponse(url="/habit-tracker", status_code=303)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

#register
@router.post("/register", response_class=HTMLResponse)
def register(
    request: Request,
    response: Response,
    r_login: str = Form(...),
    r_password: str = Form(...),
    r_password2: str = Form(...),
    db: Session = Depends(get_db)
):
    if r_password != r_password2:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "Hasła nie są takie same"},
            status_code=400
        )

    #sprawdzenie czy login jest zajęty
    existing_user = db.query(User).filter(User.login == r_login).first()
    if existing_user:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "login jest zajęty!"},
            status_code=400
        )

    hashed_password = hash_password(r_password)
    new_user = User(login=r_login, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"id": new_user.user_id, "sub": new_user.login})
    response.set_cookie(key="access_token", value=token, httponly=True)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "message": "Utworzono użytkownika! Możesz się teraz zalogować."}
    )

#chroniona ścieżka do habit-trackera
@router.get("/habit-tracker", response_class=HTMLResponse)
def habit_tracker(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/", status_code=303)

    payload = verify_access_token(token)
    if not payload:
        return RedirectResponse(url="/", status_code=303)

    user = db.query(User).filter(User.user_id == payload.get("id")).first()
    if not user:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        "habit_tracker.html",
        {"request": request, "user_id": user.user_id, "login": user.login}
    )

#wylogowanie
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response
