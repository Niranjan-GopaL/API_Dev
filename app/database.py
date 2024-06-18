from fastapi import HTTPException, status
from sqlite3 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# All DB HAS A URL with format similar to :-
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/Learning-API-dev"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"    

# what helps ORM to connect to DB
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": True}   # this is only needed for SQLite
)

"""
- assuming that each thread would handle an independent request
- But in FastAPI, using normal functions (def) MORE THAN ONE THREAD could interact with the DB for the `SAME REQUEST`
- Also, we will make sure 
    each request gets its own DB connection session IN A DEPENDENCY, 
"""

# NOTE :- 
# The key point : Now every time we perform a PATH OPERATION,
# { we use this function to create new session and connect to DB } !!!
def get_db():
    db = SessionLocal()
    try:
        yield db
    except OperationalError as e:
         raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database connection failed. Please try again later...")
    finally:
        db.close()

# Everytime we want to talk to DB => we create a new session, => which will create a new connection ; 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  we will inherit from this class to create each of the database models or classes 
Base = declarative_base()