from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from pydantic import ValidationError
from starlette.responses import JSONResponse

from database import SessionLocal
from models import User
from schemas import LoginForm, RegisterForm
from utils import verify_password, hash_password, create_access_token, verify_access_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")

#funkcja do pobierania sesjji DB
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

#pobranie akualnego uzytkownika
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

# logowanie
@router.post("/login")
async def login(
        request: Request,
        response: Response,
        login: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    try:
        form_data = LoginForm(login=login, password=password)
    except ValidationError as e:
        errors = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])

        # Check if request is from API (has Origin header from different origin)
        origin = request.headers.get("origin")
        if origin and origin != request.base_url:
            raise HTTPException(status_code=400, detail=f"Błędne dane: {errors}")

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": f"Błędne dane: {errors}"},
            status_code=400
        )

    user = db.query(User).filter(User.login == form_data.login).first()
    if not user:
        origin = request.headers.get("origin")
        if origin and origin != request.base_url:
            raise HTTPException(status_code=404, detail="Nie ma takiego użytkownika")

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "Nie ma takiego użytkownika"},
            status_code=404
        )

    if not verify_password(form_data.password, user.password):
        origin = request.headers.get("origin")
        if origin and origin != request.base_url:
            raise HTTPException(status_code=403, detail="Błędne hasło")

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "Błędne hasło"},
            status_code=403
        )

    token = create_access_token({"id": user.user_id, "sub": user.login})

    # Check if this is an API request (cross-origin)
    origin = request.headers.get("origin")
    if origin and origin != request.base_url:
        # Return JSON for API requests
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            samesite="lax"  # Important for cross-origin cookies
        )
        return {"success": True, "message": "Logged in successfully"}

    # Return redirect for same-origin form submissions
    redirect_response = RedirectResponse(url="/habit-tracker", status_code=303)
    redirect_response.set_cookie(key="access_token", value=token, httponly=True)
    return redirect_response


@router.post("/register")
async def register(
        request: Request,
        response: Response,
        r_login: str = Form(None),
        r_password: str = Form(None),
        r_password2: str = Form(None),
        db: Session = Depends(get_db)
):
    # Check if it's an API request (cross-origin)
    origin = request.headers.get("origin")
    is_api_request = origin and origin != str(request.base_url).rstrip('/')

    # Validate input
    if not r_login or not r_password or not r_password2:
        if is_api_request:
            raise HTTPException(status_code=400, detail="All fields are required")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "Wszystkie pola są wymagane"},
            status_code=400
        )

    # Validate with Pydantic
    try:
        form_data = RegisterForm(login=r_login, password=r_password, password2=r_password2)
    except ValidationError as e:
        errors = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
        if is_api_request:
            raise HTTPException(status_code=400, detail=f"Błędne dane: {errors}")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": f"Błędne dane: {errors}"},
            status_code=400
        )

    # Check if passwords match
    if form_data.password != form_data.password2:
        if is_api_request:
            raise HTTPException(status_code=400, detail="Hasła nie są takie same")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "Hasła nie są takie same"},
            status_code=400
        )

    # Check if user already exists
    existing_user = db.query(User).filter(User.login == form_data.login).first()
    if existing_user:
        if is_api_request:
            raise HTTPException(status_code=400, detail="Login jest zajęty!")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "Login jest zajęty!"},
            status_code=400
        )

    # Create new user
    hashed_password = hash_password(form_data.password)
    new_user = User(login=form_data.login, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create token
    token = create_access_token({"id": new_user.user_id, "sub": new_user.login})

    # Return appropriate response
    if is_api_request:
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            samesite="lax"
        )
        return JSONResponse(
            content={
                "success": True,
                "message": "Utworzono użytkownika! Możesz się teraz zalogować.",
                "user": {"username": new_user.login}
            }
        )

    # For form submissions
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "message": "Utworzono użytkownika! Możesz się teraz zalogować."}
    )

#wylogowanie
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response

