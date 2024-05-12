from typing import Optional,List
from typing_extensions import deprecated
from fastapi import Body, FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
from random import randrange
from time import sleep
from . import models,schemas,utils
from .database import engine,SessionLocal
from .routers import post,user,auth,vote



#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


        
try:
    conn=psycopg2.connect(host="localhost",database="backendstardb",
                        user="postgres",password="Abcd_1234",
                        cursor_factory=RealDictCursor)
    curr=conn.cursor()
    print("Database Connection successful")
except Exception as error:
    print(f"Cannot connect to database error:{error}")

@app.get("/")#url path decorator
def root():
    return {"message": "Hello"}

