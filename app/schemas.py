from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr, conint

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

class PostCreate(PostBase):
   pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes=True
        
class Post(BaseModel):
    title:str
    content:str
    published:bool
    created_at:datetime
    user_id:int
    user:Optional[UserOut]
    class Config:
        from_attributes=True


class UserCreate(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None
    
class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
    
class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        from_attributes=True