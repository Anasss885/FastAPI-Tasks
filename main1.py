# main1.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from Database import create_db_and_tables
from routers import tasks
from sqlmodel import Session
from sqlalchemy import text
from datetime import datetime, timezone
import logging

#Our main file to run our project 

@asynccontextmanager # this applying asynchronus behavior 
async def lifespan(app: FastAPI):
    create_db_and_tables()  # Call your DB setup here
    yield  # This is where FastAPI actually starts running and handling incoming requests



app = FastAPI(lifespan=lifespan) #here FastAPI uses lifesapn function to runs setup befor yield and starts serving on app and eventually it used it cleaningUp after shutdown

# Include tasks router
app.include_router(tasks.router) #this line essentially activates or attaches those grouped endpoints from tasks.py into main application



# Root endpoint with info and available endpoints
@app.get("/")
def root():
    return {
        "message": "Welcome to the Task Management API",
        "description": "This API lets you manage tasks with full CRUD functionality using FastAPI + SQLModel + SQLite.",
        "endpoints": {
            "GET /tasks": "Retrieve all tasks (supports optional pagination with query params: skip, limit)",
            "GET /tasks/{task_id}": "Retrieve a specific task by ID",
            "POST /tasks": "Create a new task",
            "PUT /tasks/{task_id}": "Update an existing task",
            "DELETE /tasks/{task_id}": "Delete a task by ID",
            "GET /health": "Check API health status and DB connection",
            "GET /tasks/status/{status}": "Retrieve tasks filtered by status",
            "GET /tasks/priority/{priority}": "Retrieve tasks filtered by priority"
        },
        "version": "v1.0"
    }

# Health check endpoint to verify API and DB status
@app.get("/health")
def health_check():
    try:
        with Session(tasks.engine) as session:
            session.exec(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logging.error(f"Health check DB error: {e}")  # Log error details
        db_status = "disconnected"
    return {
        "status": "ok",
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
