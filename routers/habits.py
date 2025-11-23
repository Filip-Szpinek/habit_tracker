from fastapi import APIRouter, Request, Depends, Query, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from urllib.parse import urlencode
from sqlalchemy.orm import Session, joinedload
from datetime import date, timedelta
from models import User, Habit, HabitLog
from .auth import get_current_user, get_db, wants_json

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Helper function - same as in auth.py
def is_api_request(request: Request) -> bool:
    accept = request.headers.get("accept", "")
    return "application/json" in accept or request.headers.get("sec-fetch-mode") == "cors"

# API endpoint to get habits
@router.get("/api/habits")
def get_habits_api(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Get all habits for the user
    habits = db.query(Habit).filter(Habit.user_id == user.user_id).all()
    
    # Format habits with logs
    habits_data = []
    for habit in habits:
        # Get last 30 days of logs
        logs = db.query(HabitLog).filter(
            HabitLog.habit_id == habit.id,
            HabitLog.user_id == user.user_id,
            HabitLog.date >= date.today() - timedelta(days=30)
        ).order_by(HabitLog.date.desc()).all()

        # Format logs by date
        logs_by_date = {}
        for log in logs:
            date_str = log.date.isoformat()
            if date_str not in logs_by_date:
                logs_by_date[date_str] = []
            logs_by_date[date_str].append({
                "time": "00:00",
                "count": 1,
                "completed": log.is_done
            })

        # Convert to list format
        formatted_logs = [
            {
                "date": date_str,
                "logs": logs_list
            }
            for date_str, logs_list in logs_by_date.items()
        ]

        habits_data.append({
            "id": habit.id,
            "title": habit.name,
            "description": habit.description,
            "frequency": habit.frequency,
            "amount": 1,
            "startDate": date.today().isoformat(),
            "logs": formatted_logs
        })

    return JSONResponse(content={"habits": habits_data})

#zaladowanie strony i habtow dla danego uzytkownika
@router.get("/habit-tracker")
def habit_tracker(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/", status_code=303)

    habits = db.query(Habit).filter(Habit.user_id == user.user_id).all()

    habit_log_data = []
    for habit in habits:
        logs = db.query(HabitLog).filter(
            HabitLog.habit_id == habit.id,
            HabitLog.user_id == user.user_id
        ).order_by(HabitLog.date.desc()).limit(7).all()
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
def check_habit(request: Request, habit_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        if is_api_request(request):
            raise HTTPException(status_code=401, detail="Not authenticated")
        return RedirectResponse(url="/", status_code=303)

    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user.user_id).first()
    if not habit:
        if is_api_request(request):
            raise HTTPException(status_code=404, detail="Habit not found")
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
        msg = f"Zadanie '{habit.name}' {'oznaczone jako wykonane ✓' if today_log.is_done else 'odznaczone X'}"
    else:
        new_log = HabitLog(
            habit_id=habit_id,
            user_id=user.user_id,
            date=date.today(),
            is_done=True
        )
        db.add(new_log)
        msg = f"Zadanie '{habit.name}' oznaczone jako wykonane ✓"

    db.commit()

    if is_api_request(request):
        return JSONResponse(content={"success": True, "message": msg})

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
        if is_api_request(request):
            raise HTTPException(status_code=401, detail="Not authenticated")
        return RedirectResponse(url="/", status_code=303)

    new_habit = Habit(
        user_id=user.user_id,
        name=name,
        description=description,
        frequency=frequency
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    msg = f"Habit '{name}' został dodany ✓"

    if is_api_request(request):
        return JSONResponse(content={
            "success": True,
            "message": msg,
            "habit_id": new_habit.id
        })

    url = "/habit-tracker?" + urlencode({"message": msg})
    return RedirectResponse(url=url, status_code=303)

#usuwanie habitow
@router.post("/delete-habit/{habit_id}")
def delete_habit(request: Request, habit_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        if is_api_request(request):
            raise HTTPException(status_code=401, detail="Not authenticated")
        return RedirectResponse(url="/", status_code=303)

    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user.user_id).first()
    if not habit:
        msg = "Nie znaleziono habitu X"
        if is_api_request(request):
            raise HTTPException(status_code=404, detail=msg)
    else:
        # Delete associated logs first
        db.query(HabitLog).filter(HabitLog.habit_id == habit_id).delete()
        db.delete(habit)
        db.commit()
        msg = f"Habit '{habit.name}' został usunięty X"

    if is_api_request(request):
        return JSONResponse(content={"success": True, "message": msg})

    url = "/habit-tracker?" + urlencode({"message": msg})
    return RedirectResponse(url=url, status_code=303)