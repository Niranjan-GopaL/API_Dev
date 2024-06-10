import random
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

class Post(BaseModel):
     title: str
     content: str
     
app = FastAPI()

my_posts = [
    {"id":1,"title" : "title_1", "content":"content_1"},
    {"id":2,"title" : "title_2", "content":"content_2"},
    {"id":3,"title" : "title_3", "content":"content_3"},
    {"id":4,"title" : "title_4", "content":"content_4"},
]


# ------------------------------- CHAPTER - 4 : DELETE ------------------------------------------------------- #




@app.get("/posts")   # don't need to add the slash unneccasarily 
def get_posts():
    return {"data ---> " : my_posts }


def find_post_with_id(id):
    for post in my_posts:
        if post["id"] == id:
            return post


# FASTAPI does it's magic validation and checks if whatever is sent is integer or not
@app.get("/posts/{id}") 
# we get the id passed, along with the default response
def get_posts(id : int, response : Response ):

    post = find_post_with_id(id)

    print(post) 
    post = find_post_with_id( int(id) )

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id requested {id} is not present ; Invalid id ; " )

    return {
                "THIS IS THE PATH PARAMETER => " : id, 
                "THIS IS IT'S TYPE => " : str(type(id))  ,
                f"post with id={id}" : post 
            }


# this is how to have a DEFAULT STATUS CODE
@app.post("/posts" , status_code=status.HTTP_201_CREATED )
def post_posts(post : Post):
    print(post)
    post_dict = post.model_dump()
    print(post_dict)
    
    post_dict["id"] = random.randint(1, 1_000_000_000)
    my_posts.append(post_dict)

    return {
            "data recieved by API in dictionary form " : post_dict,
            "data recieved ; now the list of posts are :- " : my_posts
        }