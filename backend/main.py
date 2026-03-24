from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import Base, engine, get_db
import crud
import schemas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Habit Tracker API is running"}


@app.post("/habits", response_model=schemas.HabitResponse)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    """
    Create a new habit.
    """
    return crud.create_habit(db=db, habit=habit)


@app.get("/habits", response_model=list[schemas.HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    """
    Return all habits.
    """
    return crud.get_habits(db=db)


@app.put("/habits/{habit_id}", response_model=schemas.HabitResponse)
def update_habit(
    habit_id: int, habit_update: schemas.HabitUpdate, db: Session = Depends(get_db)
):
    """
    Update the completion state of an existing habit.
    """
    updated_habit = crud.update_habit(
        db=db,
        habit_id=habit_id,
        habit_update=habit_update,
    )

    if updated_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    return updated_habit


@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing habit.
    """
    deleted_habit = crud.delete_habit(db=db, habit_id=habit_id)

    if deleted_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    return {"message": "Habit deleted successfully"}
