from sqlite3 import OperationalError
from sqlalchemy.orm import Session

from typing import List
from fastapi import FastAPI, HTTPException, Response, status
from uvicorn import run
from fastapi import Depends # for passing in the db_session_maker fn as a dependency


from signal import signal, SIGINT
from sys import exit

# THIS IS HOW YOU IMPORT FROM you're own  PACKAGE ;
# from . import models <-----------------------------------------------| Beware
# from .database import engine, SessionLocal  <------------------------| These SUCK ASS ; IMPORTING and STRUCTRE OF PACKAGES and SUBPACKAGES are not easy thing
# now on just use ` uvicorn app.main:app --reload` <-------------------| if that can't exit problem rises up again then spend 
#                                                                        time on this again

from app import models
from app import schema
from app.database import engine
from app.database import get_db
from app.schema import Create_User_Schema, Post_Create_Schema, Post_Response_Schema,Post_Update_Schema, Response_User_Schema


app = FastAPI()

# this engine is HOW you CRAEATE A TABLE to the db
models.Base.metadata.create_all(bind = engine)  


@app.get("/users", response_model=List[Response_User_Schema]) 
def get_all_user(db: Session = Depends(get_db)):
    query = db.query(models.User)
    print(query)
    users = query.all()
    return users

# Unprocessability Error ( 422 ) if the email that they send is not valid 
''' THis is the output if the email is not valid
{
    "detail": [
        {
            "type": "value_error",
            "loc": [
                "body",
                "email"
            ],
            "msg": "value is not a valid email address: The email address is not valid. It must have exactly one @-sign.",
            "input": "this com",
            "ctx": {
                "reason": "The email address is not valid. It must have exactly one @-sign."
            }
        }
    ]
}
'''
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=Create_User_Schema)
def create_user(new_user: Create_User_Schema, db: Session = Depends(get_db) ):
    try:
        user_recieved_and_serialised = models.User( **new_user.model_dump() )
        print(user_recieved_and_serialised)

        db.add(user_recieved_and_serialised)
        db.commit()
        db.refresh(user_recieved_and_serialised)
        
        return user_recieved_and_serialised
   
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database Unavailable, please try again later...")
 
   
# GET
@app.get("/sql_alchemy/posts", response_model=List[Post_Response_Schema])
def get_all_posts(db: Session = Depends(get_db)): 
    print(" -> Models is the module responsible for creating the TABLE ( it has all the blueprint ) ")
    print(" -> Post is the TABLE CLASS we defined ")
    
    
    # THIS IS SHOCKING ; THE data that it retrieves is JUST A SEQUEL COMMAND !!
    tHIS_IS_JUST_A_SQL_QUERY = db.query(models.Post)
    print(tHIS_IS_JUST_A_SQL_QUERY)
    """
    This is what db.query(TABLE_CLASS_NAME) does !!

    SELECT yet_another_table.id_sqlalc AS yet_another_table_id_sqlalc, yet_another_table.title AS yet_another_table_title, yet_another_table.content AS yet_another_table_content, yet_another_table.published AS yet_another_table_published, yet_another_table.created_at AS yet_another_table_created_at
    FROM yet_another_table
    """

    #               asking db to QUERY THIS TABLE ; retrieve all the DATA FROM THIS TABLE
    all_posts_data = db.query(models.Post).all()
    print("Quering completed, Data retrieved ...")
    return all_posts_data


# POST

# POST a "post"
# SQL WAY to do this is :-

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(new_post: Post):
#     try:
#         post_dict = new_post.model_dump()
#         if 'is_published' not in post_dict: post_dict['is_published'] = True
#         print(f"title: {post_dict['title']} content:{ post_dict['content']} is_published:{post_dict['is_published']}")

#         # this is the part where I got SOOO MANY internal server errors !
#         cur.execute( "INSERT INTO posts (title, content, is_published) VALUES (%s,%s,%s) RETURNING * ; ",  (post_dict['title'], post_dict['content'], post_dict['is_published'])  )
#         post_created = cur.fetchone()
#      
#         conn.commit()  
#         return { "data_received_by_API": post_dict, "data in postgres sql": post_created }
#     except Exception as e:
#         conn.rollback()  # Rollback the transaction on error
#         raise HTTPException(status_code=500, detail=str(e))

# THIS is a REALLY IMPORTANT PIECE OF CODE  ; this is what the FASTAPI uses as a VALIDATION MODEL ; 
# This is the schema
# class Post(BaseModel):
#      title: str
#      content: str
#      published : bool = True
     
@app.post("/sql_alchemy/posts", status_code=status.HTTP_201_CREATED, response_model=Post_Response_Schema)
# def create_post(new_post: models.Post, db: Session = Depends(get_db)): <--------- this is ERROR ; we can ONLY VALIDATE with Pydantic objects
# models.Post isn't a valid Pydantic model ; WE WANT THE OLD class Post for FastAPI to Validate
def create_post(new_post: Post_Create_Schema, db: Session = Depends(get_db)):
    try:
        # post = models.Post( title=new_post.title, content=new_post.content, published=new_post.published  ) <-- THIS IS WHAT IS HAPPENING UNDERNEATH
        # todo :- what is unpacking ? WHERE ELSE IS IT AS POWERFUL AS HERE ?
        post_recieved_and_serialised = models.Post( **new_post.model_dump() )
        print(post_recieved_and_serialised)

        db.add(post_recieved_and_serialised)
        db.commit()
        db.refresh(post_recieved_and_serialised)
        
        return post_recieved_and_serialised
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database Unavailable, please try again later...")



# GET {id}
@app.get("/sql_alchemy/posts/{id}", response_model=Post_Response_Schema)
def get_post(id: int, db: Session = Depends(get_db)):
    try:
        post_query = db.query(models.Post).filter(
                models.Post.id_sqlalc == id
            )
        
        # you wanna STOP once you find the first entry with the asked id since id is UNIQUE
        post = post_query.first() 
        print("This is the post that was asked by the client :-\n", post)

        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id {id} not found")
        return post
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database Unavailable, please try again later...")


# PUT {id}
@app.put("/sql_alchemy/posts/{id}")
def update_post(id: int, post_to_update: Post_Update_Schema, db: Session = Depends(get_db)):
    try:
        post_query = db.query(models.Post).filter(
                models.Post.id_sqlalc == id
            )
        post = post_query.first()
        print("This is the post that was asked by the client to update :- \n", post_query)
        
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id {id} not found")

        post_query.update(post_to_update.model_dump())
        print("IT HAS BEEN UPDATED !!!")
        db.commit()
        updated_post = post_query.first()
        return  updated_post
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database Unavailable, please try again later...")
    

# DELETE {id}
@app.delete("/sql_alchemy/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        delete_post_query = db.query(models.Post).filter(models.Post.id_sqlalc == id)
        post_to_delete = delete_post_query.first()
        if post_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id {id} not found")
        db.delete(post_to_delete)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database Unavailable, please try again later...")


def signal_handler(sig, frame):
    exit(0)

if __name__ == "__main__":
    # config = Config(app, host="127.0.0.1", port=8000, log_level="info", reload=True)
    # server = Server(config)
    run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info") 
    signal(SIGINT, signal_handler)
    # server.run()