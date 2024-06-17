from fastapi import FastAPI, HTTPException, Response, status
from uvicorn import run
from fastapi import Depends # for passing in the db_session_maker fn as a dependency

from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from psycopg2 import connect 

from signal import signal, SIGINT
from sys import exit
from time import sleep

# THIS IS HOW YOU IMPORT FROM you're own  PACKAGE ;
# from . import models <-----------------------------------------------| Beware
# from .database import engine, SessionLocal  <------------------------| These SUCK ASS ; IMPORTING and STRUCTRE OF PACKAGES and SUBPACKAGES are not easy thing
# now on just use ` uvicorn app.main:app --reload` <-------------------| if that can't exit problem rises up again then spend 
#                                                                        time on this again

from app import models
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

# this engine is HOW you CRAEATE A TABLE to the db
models.Base.metadata.create_all(bind = engine)  

# NOTE :- 
# The key point : Now every time we perform a PATH OPERATION,
# { we use this function to create new session and connect to DB } !!!
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# NOTE :-
# # @app.get("/posts/") <----- this did not work for some reason in POSTMAN and in web_browser ;
# #                            but somehow the interactive docs was fine with this too ; 
# @app.get("/posts")   # don't need to add the slash unneccasarily 
# def get_posts():
#     cur.execute(get_all_post_query)
#     # use fetchall() to get all rows ; fetchone() to get only one row WHEN you identify the row with UNIQUE ID
#     posts = cur.fetchall() 
#     print(posts)
#     return {"data " : posts }


@app.get("/sql_alchemy/posts")
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
    return {"data" : all_posts_data }


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

class Post(BaseModel):
     title: str
     content: str
     published : bool = True
     
@app.post("/sql_alchemy/posts", status_code=status.HTTP_201_CREATED)
# def create_post(new_post: models.Post, db: Session = Depends(get_db)): <--------- this is ERROR ; we can ONLY VALIDATE with Pydantic objects
# models.Post isn't a valid Pydantic model ; WE WANT THE OLD class Post for FastAPI to Validate
def create_post(new_post: Post, db: Session = Depends(get_db)):
    # post = models.Post(  )
    post = models.Post( **new_post.model_dump() )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(
            models.Post.id_sqlalc == id
        ).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return post


def signal_handler(sig, frame):
    exit(0)

if __name__ == "__main__":
    # config = Config(app, host="127.0.0.1", port=8000, log_level="info", reload=True)
    # server = Server(config)
    run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info") 
    signal(SIGINT, signal_handler)
    # server.run()