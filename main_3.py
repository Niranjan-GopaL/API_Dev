from fastapi import FastAPI
from pydantic import BaseModel


class Post(BaseModel):
     title: str
     content: str
     id : int



app = FastAPI()


# ------------------------------- CHAPTER - 3 : CRUD ------------------------------------------------------- #

# 1. Use PLURAL for endpoints !         Eg:- /posts , /users/:afqwer14121fd131gsdfvjryj21312 

my_post = [
    {"id":1,"title" : "title_1", "content":"content_1"},
    {"id":2,"title" : "title_2", "content":"content_2"},
]

@app.get("/posts/") 
def get_posts():
    # NOTE : 
    # 1. FASTAPI "serializes" the LIST into a JSON
    # 2. this is the data that is seen at :- http://127.0.0.1:8000/
    return {"data" : my_post }


@app.post("/posts")
def post_posts(post : Post):
    print(post)
    print(post.model_dump())
    my_post.append(post)
    return {""}

    