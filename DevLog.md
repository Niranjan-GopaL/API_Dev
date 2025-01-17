# Python - You could do that !?

```py
username: str = payload.get("sub")
```

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

# JWT Tokens implementation

in Oauth.py, these 2 functions create a token and give it to client
1. login_for_access_token()
2. create_access_token()

NOW YOU ONLY NEED TO CHECK if the token is valid or not :-
`async def get_current_active_user( current_user: Annotated[User, Depends(get_current_user)], ): `
> use this as a dependency in ANY path operation handler

Now any path operation handler can call get_current_active_user() :-
```py
# Profile page of the VALID USER
@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User :
    return current_user

# ITEMS of the VALID USER
@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
```


# Authentication ( using 1. Cookies (session based) and 2. JWT (token based) )

1. Session-Based Authentication

    - Methodology
        - Login: User logs in with credentials.
        - Session Creation: Server creates a session and stores it in the server's memory or database.
        - Session ID: Server sends a session ID as a cookie to the client.
        - Subsequent Requests: Client includes the session ID cookie in subsequent requests.
        - Validation: Server checks the session ID against its stored sessions to authenticate the user.

    - Visualization:
        - Server stores session info.
        - Client stores session ID in cookies.

    - Diagram Links:
        - [Session-Based Auth Diagram](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#session_cookie_example)

### 2. Token-Based Authentication
    - Methodology:
        - Login: User logs in with credentials.
        - Token Creation: Server generates a token (e.g., JWT) and signs it.
        - Token Storage: Server sends the token to the client.
        - Subsequent Requests: Client includes the token in the Authorization header of subsequent requests.
        - Validation: Server validates the token without needing to store session info.

    - Visualization:
        - Server does not store session info.
        - Client stores the token (e.g., in local storage or cookies).

    - Diagram Links:
        - [Token-Based Auth Diagram](https://jwt.io/introduction/)

### Key Differences:
    - Session-Based: Server keeps track of active sessions; client stores session ID.
    - Token-Based: Server does not store session state; client stores and sends token with each request.

- [MDN Web Docs on HTTP Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
- [JWT.io Introduction](https://jwt.io/introduction/)




# The great Divie - main is going to be split

Now main.py has 250 lines - has all the path operation handlers for 
- routes of posts
- routes of users
So we split main.py accordingly

- New Modularization
routers-----|\
&emsp;&emsp;&emsp;&emsp;&emsp;            | ---> user.py\
&emsp;&emsp;&emsp;&emsp;&emsp;            | ---> post.py

- `APIRouter()` and `FASTApi()` are the 2 main players

# API Security

- `$ pip install "passlib[bcrypt]" `
passlib can work with a lot of Algorihtms, Bcrypt is the most popular one.

- https://fastapi.tiangolo.com/tutorial/security/ <--- REALLY SIMPLE AND POWERFUL articles 
- https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ <-- FINALLY, WHY TF EVERYONE IS HELL BENT ON JWT

```py
from passlib.context import CryptContext

# specify which algo to use to hash passowrd
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