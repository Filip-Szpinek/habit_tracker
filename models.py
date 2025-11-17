from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import date

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    habits = relationship("Habit", back_populates="user", cascade="all, delete-orphan")
    logs = relationship("HabitLog", back_populates="user", cascade="all, delete-orphan")


class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)  # kolumna w bazie nazywa się "id"
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    frequency = Column(String(50))

    user = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")

    #alias dla zgodności z template i endpointami
    @property
    def habit_id(self):
        return self.id


class HabitLog(Base):
    __tablename__ = "habits_logs"
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    date = Column(Date, default=date.today)
    is_done = Column(Boolean, default=False)

    habit = relationship("Habit", back_populates="logs")
    user = relationship("User", back_populates="logs")