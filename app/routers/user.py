from sqlite3 import OperationalError
from sqlalchemy.orm import Session

from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi import Depends # for passing in the db_session_maker fn as a dependency



from app import models
from app.database import get_db
from app.schema import Create_User_Schema, Response_User_Schema
from app.utils import hash_from_util

router = APIRouter(
    # every single PATH will be prefixed with /sql_alchemy/users
    prefix="/sql_alchemy/users",

    # this is for the AWESOME FastAPI documentation ;
    # we GROUP all the path operation through this route as PSOTS 
    tags=['Users']
)


@router.get("/", response_model=List[Response_User_Schema]) 
def get_all_user(db: Session = Depends(get_db)):
    query = db.query( models.User )
    print(query)
    users = query.all()
    return users

# Unprocessability Error ( 422 ) if the email that they send is not valid 
''' THis is the output if the email is not valid
{
    "detail": [
        {
            "type": "value_error",
            "loc": [
                "body",
                "email"
            ],
            "msg": "value is not a valid email address: The email address is not valid. It must have exactly one @-sign.",
            "input": "this com",
            "ctx": {
                "reason": "The email address is not valid. It must have exactly one @-sign."
            }
        }
    ]
}
'''
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Response_User_Schema)
def create_user(new_user: Create_User_Schema, db: Session = Depends(get_db) ):
    try:
        # NOTE :- Sending a duplicate email STRAIGHT UP GIVES 500 INTERNAL SERVER ERROR ; => SERVER CRASH 

        user_recieved_and_serialised = models.User( **new_user.model_dump() )
        print(user_recieved_and_serialised)
        
        hash_password = hash_from_util(user_recieved_and_serialised.password)
        user_recieved_and_serialised.password = hash_password

        db.add(user_recieved_and_serialised)
        db.commit()
        db.refresh(user_recieved_and_serialised)
        
        return user_recieved_and_serialised
   
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database Unavailable, please try again later...")
 
 
@router.get("/{id}", response_model=Response_User_Schema)
def get_user(id : int, db: Session = Depends(get_db) ):
    try:
        query = db.query( models.User ).filter( models.User.id == id )
        print(query)
        user = query.first()
        print("This is the user that was asked by the client :-\n", user.__dict__)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id {id} not found")
        return user
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database Unavailable, please try again later...")