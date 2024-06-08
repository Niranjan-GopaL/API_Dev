### Humble Beginings 

```sh
$ python3 -m venv API
$ source API/bin/activate
$ pip install -r lib.txt
$ fastapi dev main.py
```

> You need to _SOURCE_ it ! <--- what you forget

### Reading the Docs ! 
- http://127.0.0.1:8000/docs          [ Interactive API doc by Swagger UI]
- http://127.0.0.1:8000/redoc         [ just normal doc ]
-  http://127.0.0.1:8000/openapi.json [ fast API generates all the JSON schema for ALL API ]
- API schema according to (Open API Specification )[https://github.com/OAI/OpenAPI-Specification]
    - OAPI spec DICTATES how to write your schema