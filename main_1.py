from click import pause
from fastapi import Body, FastAPI


# app is an OBJECT / instance of FASTAPI class
app = FastAPI()

# RUN THIS TO START the API server
# $ uvicorn main_1:app --reload

# ------------------------------- CHAPTER - 1 ----------------------------------------------------------- #

# THIS :- defining a path operation decorator
@app.get("/foo/bar")
async def root():
    return {"message": "Hello World"}

# Use f string syntax
# if you run this example and go to http://127.0.0.1:8000/items/foo, you will see a response of:
#       {"item_id": 3}
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


'''
- {"item_id":3}
  Notice that the value your function received (and returned) is 3, as a Python int, not a string "3".
  So, with that type declaration, FastAPI gives you automatic request "parsing".

- {"item_id": "foo"}
  if you go to the browser at http://127.0.0.1:8000/items/foo, you will see a nice HTTP error
  http://127.0.0.1:8000/docs <-- Notice that the path parameter is declared to be an integer
  All the data validation is performed under the hood by Pydantic
'''


# Here the path decorator is same for both the fn
# => only the first one will work, 
# `FIRST METHODE CATCHES THE REQUEST from that endpoint FIRST`
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]



# -------------------------------------------------------------------------------------------------------- #


# ------------------------------------ POST request and intro to POSTMAN ---------------------------------- #

# How do we retrive data from a POST request SENT TO `OUR API`
@app.post("/createpost")
def create_post():
    return {"status":"data provided for creating post recieved"}

@app.post("/create_more_post")
def create_better_post(payload: dict = Body(...)):
    # payload is JUST A dictionary ; retrun value of Body() function
    print(payload)
    
    # IRL, the data sent from the USER via POST
    # => IS SOTRED IN SOME DATABASE 
    
    return {
        "status":"data provided for creating post recieved",
        "content is this -> ": {
            "title_of_insta_post": payload["title_of_insta_post"],
            "second_param" : payload["second_param"]
            }
        }

# -------------------------------------------------------------------------------------------------------- #

 