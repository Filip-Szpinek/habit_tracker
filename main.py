from fastapi import FastAPI
from models import Base
from database import engine
from routers import auth

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth.router)
