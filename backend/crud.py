from sqlalchemy.orm import Session

import models
import schemas


def create_habit(db: Session, habit: schemas.HabitCreate):
    """
    Create and persist a new habit.
    """
    db_habit = models.Habit(
        name=habit.name,
        description=habit.description,
        completed=False,
    )
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


def get_habits(db: Session):
    """
    Return all habits ordered by newest first.
    """
    return db.query(models.Habit).order_by(models.Habit.created_at.desc()).all()


def update_habit(db: Session, habit_id: int, habit_update: schemas.HabitUpdate):
    """
    Update an existing habit's completion state.
    """
    db_habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()

    if db_habit is None:
        return None

    db_habit.completed = habit_update.completed
    db.commit()
    db.refresh(db_habit)
    return db_habit


def delete_habit(db: Session, habit_id: int):
    """
    Delete an existing habit.
    """
    db_habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()

    if db_habit is None:
        return None

    db.delete(db_habit)
    db.commit()
    return db_habit
