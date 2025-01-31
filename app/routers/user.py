from .. import models,schemas,utils
from typing import Optional,List
from typing_extensions import deprecated
from fastapi import Body, FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
from random import randrange
from time import sleep
from .. import models,schemas,utils
from ..database import engine,SessionLocal
from ..database import get_db

router=APIRouter(prefix="/users",
                 tags=["users"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    hashed_pass=utils.hash(user.password)
    user.password=hashed_pass
    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
   user=db.query(models.User).filter(models.User.id==id).first()
   if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           details=f"Not found {id}")
   return user 
    