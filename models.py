# models.py
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, Field as PydanticField, model_validator
from typing import Optional
from enum import Enum
from datetime import datetime, timezone

#this file is for our genric models that we're using through our work 

# Define Enums for status and priority
class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"    

class TaskBase(BaseModel):  # Base class for required fields associated with a Pydantic models for Validations
    title: str = PydanticField(..., max_length=200)
    description: Optional[str] = PydanticField(None, max_length=1000)
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = PydanticField(None, max_length=100)

    @model_validator(mode="before")  # Validation method for title to eject white spaces in written titles and reject the empty values
    def validate_and_clean(cls, values):
        title = values.get('title')
        if title is None or not title.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        values['title'] = title.strip()
        return values

class TaskCreate(TaskBase):  # Inherit required fields for POST requests
    pass

class Task(SQLModel, table=True):  # SQLModel with table creation , the Task is a TaskResponse of every get request want to render a report to a whole/specific tasks 
    id: Optional[int] = Field(default=None, primary_key=True)  # Auto-increment PK

    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

    status: TaskStatus = Field(default=TaskStatus.pending)
    priority: TaskPriority = Field(default=TaskPriority.medium)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = Field(default=None, max_length=100)

class TaskUpdate(BaseModel):  # For PATCH/PUT requests with optional fields
    title: Optional[str] = PydanticField(None, max_length=200)
    description: Optional[str] = PydanticField(None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = PydanticField(None, max_length=100)
