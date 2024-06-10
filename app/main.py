import random
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

class Post(BaseModel):
     title: str
     content: str
     
app = FastAPI()

# uvicorn app.

my_posts = { 
            0 : {"title" : "title_0", "content":"content_0"},
            1 : {"title" : "title_1", "content":"content_1"},
            2 : {"title" : "title_2", "content":"content_2"},
            3 : {"title" : "title_3", "content":"content_3"},
            4 : {"title" : "title_4", "content":"content_4"},
            5 : {"title" : "title_5", "content":"content_5"},
        }


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id requested {id} is not present ; Invalid id ; " )
    return {"data updated ! These are all the posts " : my_posts }


@app.get("/posts")   # don't need to add the slash unneccasarily 
def get_posts():
    return {"data ---> " : my_posts }


def find_post_with_id(id):
    if my_posts.__contains__(id) :
        return my_posts[id] 


# FASTAPI does it's magic validation and checks if whatever is sent is integer or not
@app.get("/posts/{id}") 
# we get the id passed, along with the default response
def get_posts(id : int, response : Response ):

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
    
    id = random.randint(1, 1_000)
    post_dict[id] = post_dict

    return {
            "data recieved by API in dictionary form " : post_dict,
            "data recieved ; now the list of posts are :- " : my_posts
        }