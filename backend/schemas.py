from datetime import datetime

from pydantic import BaseModel


class HabitCreate(BaseModel):
    """
    Schema for creating a new habit.
    """

    name: str
    description: str | None = None


class HabitResponse(BaseModel):
    """
    Schema for returning habit data.
    """

    id: int
    name: str
    description: str | None = None
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class HabitUpdate(BaseModel):
    """
    Schema for updating habit fields.
    """

    completed: bool
