### Git 
- you can't type EXCLAMANTIONS !! in git commit message ; so what you gotta do is 
```sh
git commit -m "Nailed it!!!!"  # <-- does not work
git commit -m "Nailed it!!!! " # <-- LEAVE SPACE between ! and "
```

- edit commit messages using `git commit --amend` THIS OEPNS AN TEXT EDITOR
```sh
git config --global core.editor "code" # <------- NOW IT OPENS THE COMMIT MESSAGE IN NEW VSC tab
```
- But be sure to have autosave OFF ; otherwise it'll always be `Aborting commit due to empty commit message.`
This is also an option _CURRENTLY USING THIS_
```sh
git config --global core.editor "nvim" 
```


### Humble Beginings 

# API Security

- `$ pip install "passlib[bcrypt]" `
passlib can work with a lot of Algorihtms, Bcrypt is the most popular one.

- https://fastapi.tiangolo.com/tutorial/security/ <--- REALLY SIMPLE AND POWERFUL articles 
- https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ <-- FINALLY, WHY TF EVERYONE IS HELL BENT ON JWT

```py
# hashing passowrd
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/sql_alchemy/users", status_code=status.HTTP_201_CREATED, response_model=Response_User_Schema)
def create_user(new_user: Create_User_Schema, db: Session = Depends(get_db) ):
    try:
        user_recieved_and_serialised = models.User( **new_user.model_dump() )
        
        # simple steps to hash password
        hashed_passwrd = pwd_context.hash(user_recieved_and_serialised.password)
        user_recieved_and_serialised.password = hashed_passwrd
        ...
```

# ORMs
<!-- READ THIS :- https://fastapi.tiangolo.com/tutorial/sql-databases/ -->
```py
# Every time API needs to interact with the server ; WE CREATE A NEW SESSION ; EFFICIENCY !!!
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
``` 

- When the *context* is _entered_, it creates a new `SessionLocal object` and assigns it to the variable `db`. 
- When the *context* is _exited_, it calls the close method on the db object to close the session. 
- The [yield} statement allows the `function` to be used as a `generator`, allowing the _caller to use the db object_ within a `with` statement. 





#### Postgres Beginings
```sh
$ sudo service postgresql start
$ sudo -i -u postgres      # switch to postgres user
$ createdb mydb
$ exit
```

sudo nvim /etc/postgresql/14/main/pg_hba.conf

`$ pip install psycopg2-binary` <--- if this does not work ; might need to go to normal environment and not wsl

> THIS WAS REALLY HARD and I didn't want to spend fk tonne of time in here ;
> connecting POSTGRES through wsl was not hard ; So migrated to the comfyness of Windows


#### VENV set up with FASTAPI
```sh
$ python3 -m venv API
$ source API/bin/activate
$ pip install -r lib.txt
$ fastapi dev main.py
```

Shows you all the pacakages installed 
```sh
pip freeze
```
> You need to _SOURCE_ it ! <--- what you forget

### Reading the Docs ! 

#### Theory
- http://127.0.0.1:8000/docs          [ Interactive API doc by Swagger UI]
- http://127.0.0.1:8000/redoc         [ just normal doc ]
-  http://127.0.0.1:8000/openapi.json [ fast API generates all the JSON schema for ALL API ]
- API schema according to (Open API Specification )[https://github.com/OAI/OpenAPI-Specification]
    - OAPI spec DICTATES how to write your schema


#### Code    
- FASTAPI : class PROVIDES all FUNCTIONALITY FOR your API
- A "path" is also commonly called an "endpoint" or a "route".
    - @app.get("/foo/bar")
        - path is basically `http://127.0.0.1:8000/foo/bar`
        - this is the endpoint
- While building an API, 
    > the "path" is the main way to separate "concerns" and "resources".
- In the HTTP protocol, you can communicate to each path 
  using one (or more) of these "methods".
  In OpenAPI, each of the HTTP methods is called an "operation".
    - POST
    - GET
    - PUT
    - DELETE
    - or unheard of ones :-
        - TRACE
        - PATCH
    - we were using `GET` in @app.`get`("/foo/bar")

- The `@app.get("/") tells FastAPI` function right below is in charge of handling requests that go to:
    - the `path /`
    - using a `get` operation
- A `decorator` takes the fn below and `does something` with it.
    - In our case, this decorator `tells FastAPI` that the function below 
        - corresponds to the path / 
        - with an operation get

>[!IMPORTANT]
> The information here is presented as a guideline, not a requirement.
> For example, when using GraphQL you normally perform all the actions using only POST operations.