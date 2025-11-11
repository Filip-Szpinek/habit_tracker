from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key = True, index = True)
    login = Column(String(50), unique = True, nullable = False)
    password = Column(String(255), nullable = False)