# database.py
from sqlmodel import SQLModel, create_engine, Session

# SQLite database filename - this file will store all task data persistently
sqlite_file_name = "tasks.db"

# Database URL string for SQLModel/SQLAlchemy engine configuration
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Create the SQLModel engine to interact with the SQLite database
# echo=True enables logging of SQL statements in the console for debugging
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    """
    Create database tables based on all SQLModel models' metadata.
    This function creates the necessary tables if they don't already exist.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Generator function to provide a database session.
    Used for dependency injection in FastAPI endpoints helping each request to deal with DB indirectly.
    It manages session lifecycle by opening and closing automatically.
    """
    with Session(engine) as session:
        yield session
