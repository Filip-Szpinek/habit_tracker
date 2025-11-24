import subprocess
import os
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

from models import Base
from database import engine
from routers import auth, habits

templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(habits.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Mount static files from ui/static
ui_static_path = Path("ui/static")
if ui_static_path.exists():
    app.mount("/app/assets", StaticFiles(directory="ui/static/assets"), name="ui-assets")

    # Also mount vite.svg and other root files
@app.get("/app/vite.svg")
async def serve_vite_svg():
    svg_path = ui_static_path / "vite.svg"
    if svg_path.exists():
        return FileResponse(svg_path)
    return FileResponse("ui/static/assets/vite.svg")  # fallback

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

# routing dla svelte app np. app/#/home, app/#/settings
@app.get("/app/{full_path:path}", response_class=HTMLResponse)
async def serve_app(full_path: str):
    """Serve the built Svelte app for any /app route"""
    index_path = Path("ui/static/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    return HTMLResponse(
        content="<h1>App not built yet</h1><p>Run 'npm run build' in ui folder.</p>",
        status_code=404
    )

#strona główna frontendu
@app.get("/app", response_class=HTMLResponse)
async def serve_app_root():
    """Serve the built Svelte app root"""
    index_path = Path("ui/static/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    return HTMLResponse(
        content="<h1>App not built yet</h1><p>Run 'npm run build' in ui folder.</p>",
        status_code=404
    )