from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from app.schema import Token, TokenData

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


test_users_db = {
    "johndoe": {
        "username": "johndoe",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user









# -----------------------------   2 IMPORTANT FUNCTIONS -----------------------------------------------------

#           login_for_access_token() => gives the access token to a VALID USER
#              create_access_token() => creates a jwt Token that will be used by login_for_access_token()

# THIS IS THE MOST IMPORTANT PART OF CODE WE ARE FOCUSING ON

# to create a token, we need => ` metadata + payload ` i.e DATA ` + signature ` i.e SIGNATURE
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str :

    # making a copy of the data ( so that original does not get tampered with )
    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES // 2 )
        expire = datetime.now(timezone.utc) + timedelta(minutes = 15 )


    to_encode.update({"exp": expire})
    
    # CREATED A TOKEN !!
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt

# VERY IMPORTANT PART
@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    incorrect_credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # get user from DB
    user = authenticate_user(test_users_db, form_data.username, form_data.password)

    # if user not found => raise exception
    if not user:
        raise incorrect_credential_exception

    # create an ACCESS TOKEN ( a jwt token is created here ), if the VALID USER IS LOGGING IN !
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # return the token BACK TO THE CLIENT
    return Token(access_token=access_token, token_type="bearer")








# -------------------------------  NOW WE CAN PERFOEM ALL THE PATH OEPRATION THAT ONLY A VLID USER CAN DO ----------------------------------------

# The API ROUTES that the valid users can access, begins here
# FOR BOTH WE PASS THE DEPENDENCY => ` get_current_active_user ` 

# each path operation has a dependency     => ` Depends(get_current_active_user) `
# get_current_active_user has a dependency =>  `Depends(get_current_user)` 
# { which is used to ensure that the user is authenticated and active }

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(test_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user( current_user: Annotated[User, Depends(get_current_user)], ):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


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