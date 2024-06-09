from typing import Optional
from fastapi import FastAPI
# from pydantic import BaseModel
import pydantic 
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

class Post(pydantic.BaseModel):
            # FASTAPI checks wheather the recieved data 
            #           - has "title" param 
            #           - title is a str type 
            # ( NOTE : if we pass  title: 3 then FASTAPI does an implicit converison to str (higher up) ) 
     title: str
     content: str
     category : str
     is_published : bool = True # default value
     rating : Optional[int] = None



@app.post("/create_more_post")
# now FastAPI automatically does data validation, against Post Class 
def create_better_post(new_post: Post):
    
    
    # if client send data that is INVALID ( does not respect the schema )
    # we see it in POSTMAN, there will be some error
    
    print(new_post)
    # you can CONVERT any PYDANTIC object to A DICTIONARY
    print(new_post.model_dump());
    # new_post[""]
    
    return {
        "status": f"Data recieved at :- {strftime('%Y-%m-%d %H:%M:%S', localtime()) } ",
        "content is this -> ": {
            "title"        :  new_post.title,
            "content"      :  new_post.content,
            "category"     :  new_post.category,
            "is_published" :  new_post.is_published,
            "rating" :  new_post.rating
            }
        }
