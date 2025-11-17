from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Base
from database import engine
from routers import auth, habits

templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(habits.router)

#obsluga bledu 422
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": "Błąd 422 – niepoprawne dane w formularzu"
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )