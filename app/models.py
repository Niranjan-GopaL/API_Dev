from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text
from .database import Base

""" MAJOR DISADVANTAGE OF SQLALCHEMY:
-> if it DOES NOT find the table_name then it will create it,
    BUT if a TABLE ALREADY EXISTS with that name, even if we modify the structure of the calss table_name
    SQLAlchemy won't make those changes to the existing table
-> Alembic handles DB Migration ; SQLAlchemy does not support these
-> does not support nested relationships
"""
class Post(Base):
    __tablename__ = "yet_another_table"

    id_sqlalc  =  Column(Integer, nullable=False, primary_key=True )
    title      =  Column(String, nullable=False)
    content    =  Column(String, nullable=False)
    published  =  Column(Boolean, nullable=False, server_default='TRUE')
    # if you make any changes it won't be reflected in the postgres IF THE TABLE IS ALREADY CREATED 
    created_at =  Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = "users"
    # can't have same email twice ;  
    name        = Column(String, nullable=False)
    id          = Column(Integer,nullable=False, primary_key=True)  
    email       = Column(String, nullable=False, unique=True) 
    password    = Column(String, nullable=False )
    created_at  = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))