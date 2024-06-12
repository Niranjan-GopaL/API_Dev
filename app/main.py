from fastapi import FastAPI, HTTPException, Response, status
from uvicorn import Config, Server

from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from psycopg2 import connect 

from signal import signal, SIGINT
from sys import exit
from time import sleep


app = FastAPI()

    
while True:
    try :
        # USE DOTENV and fill these data; you can have a; .env ; .env_for_development; .env_for_production; .env_for_testing
        conn = connect(
            host="localhost", 
            database="Learning-API-dev", 
            user="postgres", 
            password="123", 
            cursor_factory=RealDictCursor
        )  
        
        conn.autocommit = False  # Disable auto commit for transaction handling

        cur = conn.cursor()
        cur.execute('SELECT * FROM posts ; ')
        records = cur.fetchall()
        print(records)
        print("\n\nTestSQL Query completed correctly !!----------------------------------------------------\n\n")
        break  # the only way for this loop to end is if IT SUCCESSFULLY CONNECTS to the db
    
    except Exception as error_var :
        print("Failed to connect to DB ...")
        print("Error :- \n ", error_var)
        # 2 seconds() before trying again
        sleep(2)  

    
class Post(BaseModel):
     title: str
     content: str
     is_published : bool = True
          
# uvicorn app.main:app --reload ; 
# <package_name>.<file_name>:<FAST_API instance> 
# app.main:app --reload 

get_all_post_query  = 'SELECT * FROM posts ; '
get_id_post_query   = lambda id: f'SELECT * FROM posts WHERE id = {id}'
post_query          = lambda title, content, published: f'INSERT INTO posts (title, content, published) VALUES ({title}, {content}, {published}) RETURNING * ; '

my_posts = { 
            0 : {"title" : "title_0", "content":"content_0"},
            1 : {"title" : "title_1", "content":"content_1"},
            2 : {"title" : "title_2", "content":"content_2"},
            3 : {"title" : "title_3", "content":"content_3"},
            4 : {"title" : "title_4", "content":"content_4"},
            5 : {"title" : "title_5", "content":"content_5"},
        }


# NOTE :-
# @app.get("/posts/") <----- this did not work for some reason in POSTMAN and in web_browser ;
#                            but somehow the interactive docs was fine with this too ; 
@app.get("/posts")   # don't need to add the slash unneccasarily 
def get_posts():
    cur.execute(get_all_post_query)
    # use fetchall() to get all rows ; fetchone() to get only one row WHEN you identify the row with UNIQUE ID
    posts = cur.fetchall() 
    print(posts)
    return {"data " : posts }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT )
def delete_post(id:int):
    print(my_posts)

    # trying to delete with a key that's not present gives => INTERNAL server error
    if my_posts.__contains__(id):
        my_posts.pop(id)
        # del my_posts[id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id requested {id} is not present ; Invalid id ; " )

    # for 204, we don't expect ANY return from the API to the client



# with put,  NOTE :- even if you wanna update only field, you'll need to pass in everything
@app.put("/posts/{id}")
def update_post(updated_post:Post, id: int):
    if my_posts.__contains__(id):
        my_posts[id] = updated_post.model_dump()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the id requested {id} is not present ; Invalid id ; " 
        )
    return {"data updated ! These are all the posts " : my_posts }




# FASTAPI does it's magic validation and checks if whatever is sent is integer or not
@app.get("/posts/{id}") 
# we get the id passed, along with the default response
def get_posts(id : int, response : Response ):

    # Findings a post with a given id in Postgre SQL
    # even if the id is invalid the QUery will execute correctly !!
    cur.execute( get_id_post_query(int(id)) )
    post = cur.fetchone()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id requested {id} is not present ; Invalid id ; " )

    return {
                "THIS IS THE PATH PARAMETER => " : id, 
                "THIS IS IT'S TYPE => " : str(type(id))  ,
                f"post with id={id}" : post 
            }



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    try:
        print("Post recieved : ", new_post, "\n\n----------------------------------------------------------------------\n\n\n")
        post_dict = new_post.model_dump()
        print("Post in dict() : ", post_dict, "\n\n----------------------------------------------------------------------\n\n")
        if 'is_published' not in post_dict: post_dict['is_published'] = True
        print(f"title: {post_dict['title']} content:{ post_dict['content']} is_published:{post_dict['is_published']}")

        # this is the part where I got SOOO MANY internal server errors !
        cur.execute(
                    "INSERT INTO posts (title, content, is_published) VALUES (%s,%s,%s) RETURNING * ; ", 
                    (post_dict['title'], post_dict['content'], post_dict['is_published']) 
                    )
        
        # Here lies my unsafe but REALLY FKING CLEAN code 😢💔 ;
        # This absolutely works ; But we don't use it since it's prone to SQL injections ?
        # cur.execute(
        #     post_query(
        #         post_dict['title'],
        #         post_dict['content'],
        #         post_dict['is_published']
        #     )
        # )
        
        post_created = cur.fetchone()
        print(post_created,"\n\n\n")

        # VERY IMPORTANT !! Commit the transaction on success ; we are did conn.autocommit = False => we need to do it OURSELVES
        conn.commit()  

        return {
            "data_received_by_API": post_dict,
            # THIS IS SERIALIZED by FASTAPI !! 
            "data in postgres sql": post_created
        }
    except Exception as e:
        conn.rollback()  # Rollback the transaction on error
        raise HTTPException(status_code=500, detail=str(e))



def signal_handler(sig, frame):
    conn.close()
    exit(0)

if __name__ == "__main__":
    config = Config(app, host="127.0.0.1", port=8000, log_level="info", reload=True)
    server = Server(config)
    signal(SIGINT, signal_handler)
    server.run()