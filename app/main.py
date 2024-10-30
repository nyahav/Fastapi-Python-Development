from fastapi import  FastAPI, HTTPException,Response,status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas,util
from .database import engine,get_db
from .routers import post,user,auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#video stopped at 6:03:10

# class Post(BaseModel):
#     title: str
#     content: str
#     published : bool = True
    

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='password',cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
            print("Database connection was unsuccesfull")
            print("Error:", error)
            time.sleep(2)

'''
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
'''
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
@app.get("/")
async def root():
    return {"message":"welcome to my api!"}


