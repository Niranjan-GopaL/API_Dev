### Humble Beginings 

```sh
$ python3 -m venv API
$ source API/bin/activate
$ pip install -r lib.txt
$ fastapi dev main.py
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