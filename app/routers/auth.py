from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from app.schema import Create_User_Schema

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: Create_User_Schema = Depends(), db: Session = Depends(database.get_db)):

    query = db.query(models.User).filter(models.User.email == user_credentials.email)
    user  = query.first()

    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token
    