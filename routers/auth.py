from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from pydantic import ValidationError
from database import SessionLocal
from models import User
from schemas import LoginForm, RegisterForm
from utils import verify_password, hash_password, create_access_token, verify_access_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# funkcja do pobierania sesjji DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# strona główna
# @router.get("/app/", response_class=HTMLResponse)
# def login_form(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# pobranie akualnego uzytkownika
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        return None

    payload = verify_access_token(token)
    if not payload:
        return None

    user_id = payload.get("id")
    if not user_id:
        return None

    user = db.query(User).options(joinedload(User.habits)).filter(User.user_id == user_id).first()
    if not user:
        return None

    return user


# Helper function - check if Accept header wants JSON
def wants_json(request: Request) -> bool:
    accept = request.headers.get("accept", "")
    # Check if client accepts JSON or if it's a fetch request
    return "application/json" in accept or request.headers.get("sec-fetch-mode") == "cors"


# ###login - Always return JSON for API calls
@router.post("/login")
def login(
        request: Request,
        login: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    try:
        form_data = LoginForm(login=login, password=password)
    except ValidationError as e:
        errors = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
        if wants_json(request):
            raise HTTPException(status_code=400, detail=f"Błędne dane: {errors}")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": f"Błędne dane: {errors}"},
            status_code=400
        )

    user = db.query(User).filter(User.login == form_data.login).first()
    if not user:
        if wants_json(request):
            raise HTTPException(status_code=404, detail="Nie ma takiego użytkownika")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "Nie ma takiego użytkownika"},
            status_code=404
        )

    if not verify_password(form_data.password, user.password):
        if wants_json(request):
            raise HTTPException(status_code=403, detail="Błędne hasło")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "Błędne hasło"},
            status_code=403
        )

    token = create_access_token({"id": user.user_id, "sub": user.login})

    # For JSON requests (from Svelte app)
    if wants_json(request):
        response = JSONResponse(content={
            "success": True,
            "message": "Logged in successfully",
            "user": {"username": user.login}
        })
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=3600 * 24 * 7,
            path="/"
        )
        return response

    # For form submissions from HTML templates
    redirect_response = RedirectResponse(url="/habit-tracker", status_code=303)
    redirect_response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        path="/"
    )
    return redirect_response


# ###register - Always return JSON for API calls
@router.post("/register")
def register(
        request: Request,
        r_login: str = Form(...),
        r_password: str = Form(...),
        r_password2: str = Form(...),
        db: Session = Depends(get_db)
):
    try:
        form_data = RegisterForm(login=r_login, password=r_password, password2=r_password2)
    except ValidationError as e:
        errors = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
        if wants_json(request):
            raise HTTPException(status_code=400, detail=f"Błędne dane: {errors}")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": f"Błędne dane: {errors}"},
            status_code=400
        )

    if form_data.password != form_data.password2:
        if wants_json(request):
            raise HTTPException(status_code=400, detail="Hasła nie są takie same")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "Hasła nie są takie same"},
            status_code=400
        )

    existing_user = db.query(User).filter(User.login == form_data.login).first()
    if existing_user:
        if wants_json(request):
            raise HTTPException(status_code=400, detail="Login jest zajęty!")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "Login jest zajęty!"},
            status_code=400
        )

    hashed_password = hash_password(form_data.password)
    new_user = User(login=form_data.login, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"id": new_user.user_id, "sub": new_user.login})

    # For JSON requests (from Svelte app)
    if wants_json(request):
        response = JSONResponse(content={
            "success": True,
            "message": "Utworzono użytkownika!",
            "user": {"username": new_user.login}
        })
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=3600 * 24 * 7,
            path="/"
        )
        return response

    # For form submissions from HTML templates
    redirect_response = RedirectResponse(url="/", status_code=303)
    redirect_response.set_cookie(key="access_token", value=token, httponly=True, path="/")
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "message": "Utworzono użytkownika! Możesz się teraz zalogować."}
    )


# wylogowanie
@router.get("/logout")
def logout(request: Request):
    if wants_json(request):
        response = JSONResponse(content={"success": True, "message": "Logged out"})
    else:
        response = RedirectResponse(url="/", status_code=303)

    response.delete_cookie(key="access_token", path="/")
    return response