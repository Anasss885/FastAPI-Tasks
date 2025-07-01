# crud.py
from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate
from datetime import datetime, timezone

#this pyhton file contains all Crud operations 

#below function handle the post request by creating a new task from scratch 
def create_task(session: Session, task_create: TaskCreate) -> Task:
    new_task = Task(
        title=task_create.title.strip(),
        description=task_create.description,
        status=task_create.status,
        priority=task_create.priority,
        due_date=task_create.due_date,
        assigned_to=task_create.assigned_to,
        created_at=datetime.now(timezone.utc),
        updated_at=None
    )
    session.add(new_task) #working on the task 
    session.commit() # added the task in DBMS physically , after get it finished
    session.refresh(new_task)
    return new_task

#the below function handle the get request to all functions without any type of filtration
def get_all_tasks(session: Session, skip: int = 0, limit: int = 10):
    statement = select(Task).offset(skip).limit(limit)
    return session.exec(statement).all() #(i.e select * )

#below function handles getting a specific function using its id
def get_task_by_id(session: Session, task_id: int):
    return session.get(Task, task_id)

#below function handles put request as we can update any task we want , it also support partial updating (Patching)
def update_task(session: Session, existing_task: Task, task_update: TaskUpdate):
    updated_data = existing_task.model_dump() #model_dump() , converts our plain to dictionary structure to deal with it in a more proper,easy,safer way
    update_fields = task_update.model_dump(exclude_unset=True) #converts the updated attributes only to dict
    updated_data.update(update_fields) #applying the updated values to our dictionary format scope
    updated_data["updated_at"] = datetime.now(timezone.utc)
    for key, value in updated_data.items():
        setattr(existing_task, key, value) # to save our changes back to its plain format to be able to add it back to our DB 
    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)
    return existing_task

def delete_task(session: Session, task: Task):
    session.delete(task)
    session.commit()

def get_tasks_by_status(session: Session, status: str, skip: int = 0, limit: int = 10):
    statement = select(Task).where(Task.status == status).offset(skip).limit(limit)
    return session.exec(statement).all()

def get_tasks_by_priority(session: Session, priority: str, skip: int = 0, limit: int = 10):
    statement = select(Task).where(Task.priority == priority).offset(skip).limit(limit)
    return session.exec(statement).all()
