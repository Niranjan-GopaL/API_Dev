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

# @app.get("/posts/") <----- this did not work for some reason in POSTMAN and in web_browser ; but somehow the interactive docs was fine with this too ; 
@app.get("/posts")   # don't need to add the slash unneccasarily 
def get_posts():
    # NOTE : 
    # 1. FASTAPI "serializes" the LIST into a JSON
    # 2. this is the data that is seen at :- http://127.0.0.1:8000/
    # return {"data ---> " : my_posts }
    return {"data ---> " : my_posts }


@app.get("/posts/{id}") 
def get_posts(id):
    # fn to do this :- ZERO TASK
    # retriving the post  with that ID 
    

    # FIRST TASK :-
    # you'll get None error without explicit conversion since function checks id === my_posts[i]["id"]
    # NOTE: REMEMBER ID <---------- STRING ; MANUALLY **EXPLICITLY CONVERT IT**

    # SECOND TASK
    # But we also need to make sure that passed parameter, id CAN BE CONVERTED TO INTEGER
    # Otherwise int() will give an error <---- INTERNAL SERVER ERROR
    # Ans : def get_posts(id : int)      <---- FAST-API will validate this 
    #                                   ; Now on passing a string as a path parameter 
    #                                   ; Front ed gets a nice error requesting only string parameters

    # FOURTH : How important is ordering
    # THIS IS WRONG  <---- if user goes to /posts/latest ; server matches it with /posts/{id} 
    # @app.get(/posts/{id})
    # @app.get(/posts/latest)

    # FIFTH : there is no way for front end to know if there was an out of bound error ;
    # the user can go to /posts/10000 even if there are only 10 posts ; we want front end to know this 
    # Ans : 404 error code ; the path DOES NOT EXIST ; 
    # More : we wanna send these [best practices]
    # ; 200ish status codes seem to send OK 
    # ; 400ish are not found ERRORS 
    # ; 500ish are SERVER errors 
    # 1-------> use Response, Status lib
    # 2-------> use HTTPException [ REALLY CLEAN and CONCISE ]


    # SIXTH : now every time you create a post, send the correct HTTP status code ( 201 )
    # how to pass in default status code

    return {
        "THIS IS THE PATH PARAMETER => " : id, 
        "THIS IS IT'S TYPE => " : type(id) 
            }

 
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