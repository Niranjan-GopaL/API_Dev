import random
from fastapi import FastAPI, HTTPException, Response, status
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
    {"id":3,"title" : "title_3", "content":"content_3"},
    {"id":4,"title" : "title_4", "content":"content_4"},
]


# NOTE :-
# @app.get("/posts/") <----- this did not work for some reason in POSTMAN and in web_browser ; but somehow the interactive docs was fine with this too ; 
@app.get("/posts")   # don't need to add the slash unneccasarily 
def get_posts():
    # NOTE : 
    # 1. FASTAPI "serializes" the LIST into a JSON
    # 2. this is the data that is seen at :- http://127.0.0.1:8000/
    # return {"data ---> " : my_posts }
    return {"data ---> " : my_posts }







def find_post_with_id(id):
    for post in my_posts:
        if post["id"] == id:
            return post


# FASTAPI does it's magic validation and checks if whatever is sent is integer or not
@app.get("/posts/{id}") 
# we get the id passed, along with the default response
def get_posts(id : int, response : Response ):

    # fn to do this :- ZERO TASK
    # retriving the post  with that ID 
    post = find_post_with_id(id)

    # FIRST TASK :-
    print(post) # this will always be None ; we are passing a STRING ; we expect an INTEGER
    post = find_post_with_id( int(id) )
    

    # SECOND TASK
    # But we also need to make sure that passed parameter, id CAN BE CONVERTED TO INTEGER
    # Otherwise int() will give an error <---- INTERNAL SERVER ERROR
    # Ans : def get_posts(id : int)      <---- FAST-API will validate this 
    #                                   ; Now on passing a string as a path parameter 
    #                                   ; Front ed gets a nice error requesting only string parameters




    # THIRD : How important is ordering
    # THIS IS WRONG :-  <---- if user goes to /posts/latest ; server matches it with /posts/{id} 
    # @app.get(/posts/{id})
    # @app.get(/posts/latest)


    # FOURTH : there is no way for front end to know if there was an out of bound error ;
    # the user can go to /posts/10000 even if there are only 10 posts ; we want front end to know this 
    # Ans : 404 error code ; the path DOES NOT EXIST ; 
    # More : we wanna send these [best practices]
    # ; 200ish status codes seem to send OK 
    # ; 400ish are not found ERRORS 
    # ; 500ish are SERVER errors 
    # 1-------> use Response, Status lib
    # 2-------> use HTTPException [ REALLY CLEAN and CONCISE ]

    if post is None :
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "message" : f"post with the id requested {id} is not present ; Invalid id ; " }

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id requested {id} is not present ; Invalid id ; " )

    # FIFTH : now every time you create a post, send the correct HTTP status code ( 201 )
    # change the POST /posts  to pass in default status code when you create a resource

    
    # New lesson :- you can't do return { ..., "key" : type(id)  } since type returns something that can't be used as a VALUE 
    return {
        "THIS IS THE PATH PARAMETER => " : id, 
        "THIS IS IT'S TYPE => " : str(type(id))  , 
            }

# this is how to have a DEFAULT STATUS CODE
@app.post("/posts" , status_code=status.HTTP_201_CREATED )
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