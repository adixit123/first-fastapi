from .. import models,schemas,utils
from typing import Optional,List
from typing_extensions import deprecated
from fastapi import Body, FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session,defer,join
from pydantic import BaseModel
from sqlalchemy import func
from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
from random import randrange
from time import sleep
from .. import models,schemas,utils,oauth2
from ..database import engine,SessionLocal
from ..database import get_db

router=APIRouter(prefix="/posts",
                 tags=["posts"])

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),
              curr_user:int=Depends(oauth2.get_current_user),
              limit:int=10,skip:int=0,search:Optional[str]=""):
    posts=db.query(models.Post).filter(models.Post.title.contains(
        search)).limit(limit).offset(skip).all()
    
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).outerjoin(
        models.Vote,models.Vote.post_id==models.Post.id,).group_by(models.Post.id).filter(models.Post.title.contains(
        search)).limit(limit).offset(skip).all()
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),
                 curr_user:int=Depends(oauth2.get_current_user)):
    print(curr_user.email)
    new_post=models.Post(user_id=curr_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

"""@app.get("/posts/latest")
def get_latest_posts():
    latest=my_posts[len(my_posts)-1]
    return latest"""
 
@router.get("/{id}")
def get_post(id:int,db:Session=Depends(get_db),
            curr_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not Found Post {id}")
    return post
   
@router.delete("/{id}")
def delete_posts(id:int,db:Session=Depends(get_db),
                curr_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not found {id}")
    
    if post.user_id!=curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    db.delete(post)
    db.commit()
    return {"Message":f"Deleted post {id}"}

@router.put("/{id}")
def update(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),
            curr_user:int=Depends(oauth2.get_current_user)):
    upd_post=db.query(models.Post).filter(models.Post.id==id)
    if upd_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not found {id}")
    if upd_post.user_id!=curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    upd_post.update(post.model_dump())
    db.commit()
    return upd_post.first()

@router.get("/sqlalchemy")
def test_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"Data":posts}

