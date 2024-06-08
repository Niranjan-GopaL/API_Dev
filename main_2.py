from click import pause
from fastapi import Body, FastAPI
from pydantic import BaseModel
from time import localtime, gmtime, strftime

# app is an OBJECT / instance of FASTAPI class
app = FastAPI()

# RUN THIS TO START the API server
# $ uvicorn main_2:app --reload


# ------------------------------- CHAPTER - 2 : Schema using pydantic ------------------------------------------------------- #

'''
title : str
is_published : bool
time : str
category : str
ip : list of 4 integers
'''

class Post(BaseModel):
     title: str
     content: str
     category : str
     is_published : bool


     
@app.post("/create_more_post")
def create_better_post(new_post: Post):
    # payload is JUST A dictionary ; retrun value of Body() function
    print(new_post)
    
    return {
        "status": f"Data recieved at :- {strftime('%Y-%m-%d %H:%M:%S', localtime()) } ",
        "content is this -> ": {
            "title": new_post["title"],
            "content" : new_post["content"],
            "category" : new_post["category"],
            "is_published" : new_post["is_published"]
            }
        }
