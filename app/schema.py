from datetime import datetime
from pydantic import BaseModel, EmailStr


class Post(BaseModel):
     title: str
     content: str
     published : bool = True

# Now we can DEFINE ALL THE SCHEMAS here ( all the Pydantic models )
# Examples :-

class Create_Post(BaseModel):
    title : str
    content : str
    published : bool = True

class Update_Post(BaseModel):
    title : str
    content : str
    published : bool

# This means WE CAN SEND API REQUEST WITH ONLY title field
# def update_title_post(new_post : Update_Title_Post, db: Session = Depends(get_db) ) <----- THIS IS HOW this would be used ; 
class Update_Title_Post(BaseModel):
    title : str

class Person(BaseModel):
    id: int
    is_active: bool
    class Config:
        orm_mode = True
'''
Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, 
but an ORM model (or any other arbitrary object with attributes).

This way, instead of only trying to get the id value from a dict, as in: id = data["id"]
it will also try to get it from an attribute, as in: id = data.id
'''

 
# We can define REPONSE MODELS ( strict with what information we send back to client )

# NOW IT WON'T SEND BACK `id, created_At time`
# post = post_query.first() 
# return post <------------ all the information from db is sent ; 
# 
# WE WANT TO RESTRICT THIS ; CAN'T SEND BACK STUFF LIKE PASSWORD AND SO ON
class Post_Response_Schema(Post):
    title : str
    content : str
    published : bool = True   
    # the front end would want to render this out ;  
    created_at : datetime

# --------------------------------- REAL STUFF -------------------------------------------------------------

# An important pattern in CREATING SCHEMA :- ( using Inheritance )
class Post_Base_Schema(BaseModel):
    title : str
    content : str
    published : bool = True

# Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, 
# but an ORM model (or any other arbitrary object with attributes).
# see :- https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode  
    class Config:
        # orm_mode = True
        
# D:\Code Practise\API_Dev\API_in_win\Lib\site-packages\pydantic\_internal\_config.py:334:  Warning: Valid config keys have changed in V2:
#  'orm_mode' has been renamed to 'from_attributes'
#   warnings.warn(message, UserWarning)
        from_attributes = True

class Post_Create_Schema(Post_Base_Schema):
    pass

class Post_Update_Schema(Post_Base_Schema):
    published : bool   
    
class Post_Response_Schema(Post_Base_Schema):
    # the front end would want to render this out ;  
    published : bool   
    created_at : datetime 
    
# -------------------------- USERS ------------------------

class User(BaseModel):
    name     : str
    email    : EmailStr
    password : str
    class Config:
        from_attributes = True

class Response_User_Schema(BaseModel):
    id         : int
    created_at : datetime
    email      : EmailStr
    name       : str

class Create_User_Schema(User):
    pass