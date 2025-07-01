# routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import List
from sqlmodel import Session
from models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from crud import (
    create_task, get_all_tasks, get_task_by_id, update_task,
    delete_task, get_tasks_by_status, get_tasks_by_priority
)
from Database import get_session

#this file to handle the critical endpoints of our app 

router = APIRouter()

# POST endpoint to create task
@router.post("/tasks", response_model=Task, status_code=201)
def create_task_endpoint(task: TaskCreate, session: Session = Depends(get_session)):
    return create_task(session, task)

# GET all tasks with pagination support
@router.get("/tasks", response_model=List[Task])
def get_tasks_endpoint(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return"),
    session: Session = Depends(get_session)
):
    return get_all_tasks(session, skip, limit)

# GET task by ID
@router.get("/tasks/{task_id}", response_model=Task)
def get_task_by_id_endpoint(task_id: int, session: Session = Depends(get_session)):
    task = get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# PUT to update task
@router.put("/tasks/{task_id}", response_model=Task)
def update_task_endpoint(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    existing_task = get_task_by_id(session, task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task(session, existing_task, task_update)

# DELETE a task
@router.delete("/tasks/{task_id}")
def delete_task_endpoint(task_id: int, session: Session = Depends(get_session)):
    task = get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="The task you want to remove was not found")
    delete_task(session, task)
    return {"detail": "The task has been removed successfully!"}

# GET tasks filtered by status with pagination
@router.get("/tasks/status/{status}", response_model=List[Task])
def get_tasks_by_status_endpoint(
    status: TaskStatus = Path(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session)
):
    tasks = get_tasks_by_status(session, status, skip, limit)
    if not tasks:
        raise HTTPException(status_code=404, detail=f"No tasks with status '{status}' found")
    return tasks

# GET tasks filtered by priority with pagination
@router.get("/tasks/priority/{priority}", response_model=List[Task])
def get_tasks_by_priority_endpoint(
    priority: TaskPriority = Path(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session)
):
    tasks = get_tasks_by_priority(session, priority, skip, limit)
    if not tasks:
        raise HTTPException(status_code=404, detail=f"No tasks with priority '{priority}' found")
    return tasks
