from fastapi import FastAPI

# app is an OBJECT / instance of FASTAPI class
app = FastAPI()

# ------------------------------- CHAPTER - 1 -------------------------------------------------------------------- #

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
'''

# -------------------------------------------------------------------------------------------------------- #



@app.post("/")
async def methode_1():
    pass

@app.post("/")
async def methode_2():
    pass

