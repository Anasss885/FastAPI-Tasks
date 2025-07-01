# FastAPI-Tasks
A simple and efficient Task Management API built with FastAPI, SQLModel, and SQLite. Supports full CRUD operations, task filtering by status and priority, and pagination for scalable task handling.
------------------------------------
### 1-Setup & Testing Instructions
Follow these steps to get the Task Management API running locally:

 1. Clone the repositorys

#bash
git clone https://github.com/Anasss885/FastAPI-Tasks.git
cd FastAPI-Tasks

2. Create and activate a Python virtual environment

3. Install dependencies
pip install fastapi[all] sqlmodel

4. Run the FastAPI server
uvicorn main1:app --reload --port 8000

5. Access the API documentation
Open your browser and navigate to the interactive Swagger UI:
http://127.0.0.1:8000/docs
this step will also helps you to test all endpoints properly 

6. Database details
-The app uses SQLite, with the database file named tasks.db.
-The database and tables are created automatically when the app starts.
-To reset the database, simply delete the tasks.db file and restart the server.


Troubleshooting
Ensure Python 3.8+ is installed.
Activate the virtual environment before installing packages or running the server.
Make sure uvicorn is installed and available in your PATH.

### 2-Assumptions & Design Decisions
- The app uses SQLite as the database for simplicity and easy local setup.
- Tasks have a status and priority modeled as Enums to restrict allowed values.
- The API supports pagination with skip and limit query parameters to handle large datasets.
- Validation rules are implemented to ensure task titles are not empty and due dates (if provided) must be future dates.
- The app uses SQLModel for ORM capabilities to simplify database interactions.
- Endpoints follow RESTful conventions with proper HTTP status codes (201, 200, 404, 422, 400).
- For simplicity, all code is organized into separate files by responsibility (models, database, routes).
- The project assumes a single-user environment (no authentication or multi-user support).
- The app built on OOP concepts as
   1.Abstraction
     --it applies through:
         *Models Abstract the Data Layer:
           TaskBase, TaskCreate, and TaskUpdate hide direct field access from external users.
           You expose only relevant fields to the API consumer based on the context (creation vs update vs full task).
        *Enums Abstract Raw Status and Priority Values:
          TaskStatus and TaskPriority enums replace hardcoded strings like "pending" or "high" with clean, readable types.
        *Health Check Encapsulates DB Connection Logic:
         The /health endpoint uses session.exec(text("SELECT 1")) to check DB status.
         From outside, users just see "connected" or "disconnected", not how the check is done.
  2.Encapsulation
     --it applies through:
         *TaskBase, TaskCreate, and TaskUpdate encapsulate the rules and structure of your task data.
         *API users don’t need to know how validation is done — they just send valid data. 
         *Encapsulation in API Behavior:
           API user only interacts with high-level routes (/tasks, /health, etc.).
           They don’t see DB structure, table names, or internal logic.
           Even health check hides its SELECT 1 inside a try/except block.
  3.Inheritance
    --it applies through:
       *TaskCreate is used for POST requests to create new tasks as It inherits:
             All field definitions (title, description, etc.).
             All validation logic (@model_validator).
       *TaskUpdate Also Shares Structure of TaskBase.
  4.Polymorphism
   --it applies through:
      *Both TaskCreate and TaskUpdate :
        TaskCreate is strict (required fields).
       TaskUpdate is flexible (optional fields).
  i.e :  they are Different forms of "Task data", but treated through a common structure , That's polymorphism via inheritance and structure.

  Eventually, we will talk about the Performance of application :
    Our application leverages efficient data structures like Enums for filtering and SQLModel for structured data modeling, combining the power of Pydantic validation with SQLAlchemy ORM. We use relational tables backed by SQLite, with indexed primary key lookups ensuring constant-time access to tasks by ID. Pagination is implemented using offset and limit to prevent performance bottlenecks when handling large datasets. Each request operates within its own database session, ensuring isolated, performant interactions. Overall, the system is well-optimized for small to medium scale and can be scaled further by integrating advanced indexing, caching, or migrating to a more robust database engine like PostgreSQL.
  
         
    
