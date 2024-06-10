import random
from fastapi import FastAPI
from pydantic import BaseModel


class Post(BaseModel):
     title: str
     content: str
    #  id : int <--- this is ASSIGNED BY THE DATABSE ; the user need not send this



app = FastAPI()


# ------------------------------- CHAPTER - 3 : CRUD ------------------------------------------------------- #

# 1. Use PLURAL for endpoints !         Eg:- /posts , /users/:afqwer14121fd131gsdfvjryj21312 

my_posts = [
    {"id":1,"title" : "title_1", "content":"content_1"},
    {"id":2,"title" : "title_2", "content":"content_2"},
]

@app.get("/posts/") 
def get_posts():
    # NOTE : 
    # 1. FASTAPI "serializes" the LIST into a JSON
    # 2. this is the data that is seen at :- http://127.0.0.1:8000/
    return {"data" : my_posts }

 
@app.post("/posts")
def post_posts(post : Post):
    print(post)
    post_dict = post.model_dump()
    print(post_dict)
    
    # we need to assign everything an id ; normally this HAS TO BE  done by DB  
    post_dict["id"] = random.randint(1, 1_000_000_000)
    
    my_posts.append(post_dict)

    return {
            "data recieved by API in dictionary form " : post_dict,
            "data recieved ; now the list of posts are :- " : my_posts
        }