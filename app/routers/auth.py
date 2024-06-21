from sqlite3 import OperationalError
from sqlalchemy.orm import Session

from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi import Depends # for passing in the db_session_maker fn as a dependency

router = APIRouter(
    prefix = "/auth/login",
    tags=['Authentication']
)

@router.get("/")
def get_user_auth(  ):
    pass