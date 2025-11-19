from pydantic import BaseModel, Field

class LoginForm(BaseModel):
    login: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=4, max_length=100)

class RegisterForm(BaseModel):
    login: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=4, max_length=100)
    password2: str = Field(..., min_length=4, max_length=100)
