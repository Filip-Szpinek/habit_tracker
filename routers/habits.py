from fastapi import APIRouter, Request, Depends, Query, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from sqlalchemy.orm import Session, joinedload
from datetime import date
from models import User, Habit, HabitLog
from .auth import get_current_user, get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

#zaladowanie strony i habtow dla danego uzytkownika
@router.get("/habit-tracker")
def habit_tracker(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/", status_code=303)

    # Pobranie wszystkich habitów użytkownika
    habits = db.query(Habit).filter(Habit.user_id == user.user_id).all()

    # Pobranie logów do heatmapy
    habit_log_data = []
    for habit in habits:
        logs = db.query(HabitLog).filter(
            HabitLog.habit_id == habit.id,
            HabitLog.user_id == user.user_id
        ).order_by(HabitLog.date.desc()).limit(3).all()
        habit_log_data.append({"habit": habit, "logs": logs})

    return templates.TemplateResponse(
        "habit_tracker.html",
        {
            "request": request,
            "login": user.login,
            "user_id": user.user_id,
            "habits": habits,
            "habit_log_data": habit_log_data 
        }
    )
#checkowanie habitow
@router.post("/check-habit/{habit_id}")
def check_habit(habit_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/", status_code=303)

    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user.user_id).first()
    if not habit:
        return RedirectResponse(url="/habit-tracker", status_code=303)

    today_log = (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit_id,
            HabitLog.user_id == user.user_id,
            HabitLog.date == date.today()
        ).first()
    )

    if today_log:
        today_log.is_done = not today_log.is_done
        if today_log.is_done:
            msg = f"Zadanie '{habit.name}' oznaczone jako wykonane ✔"
        else:
            msg = f"Zadanie '{habit.name}' odznaczone X"
    else:
        new_log = HabitLog(
            habit_id=habit_id,
            user_id=user.user_id,
            date=date.today(),
            is_done=True
        )
        db.add(new_log)
        msg = f"Zadanie '{habit.name}' oznaczone jako wykonane ✔"

    db.commit()

    url = "/habit-tracker?" + urlencode({"message": msg})
    return RedirectResponse(url=url, status_code=303)

#dodawanie nowych habitow
@router.post("/add-habit")
def add_habit(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    frequency: str = Form(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        return RedirectResponse(url="/", status_code=303)

    new_habit = Habit(
        user_id=user.user_id,
        name=name,
        description=description,
        frequency=frequency
    )
    db.add(new_habit)
    db.commit()

    msg = f"Habit '{name}' został dodany ✔"
    url = "/habit-tracker?" + urlencode({"message": msg})
    return RedirectResponse(url=url, status_code=303)

#usuwanie habitow
@router.post("/delete-habit/{habit_id}")
def delete_habit(habit_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/", status_code=303)

    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user.user_id).first()
    if not habit:
        msg = "Nie znaleziono habitu X"
    else:
        db.delete(habit)
        db.commit()
        msg = f"Habit '{habit.name}' został usunięty X"

    url = "/habit-tracker?" + urlencode({"message": msg})
    return RedirectResponse(url=url, status_code=303)
