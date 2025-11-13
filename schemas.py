from pydantic import BaseModel, Field, constr

class LoginForm(BaseModel):
    login: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=4, max_length=255)
