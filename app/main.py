from fastapi import  FastAPI, HTTPException,Response,status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



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

my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favorite foods","content":"I like pizze","id":2}]
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
@app.get("/")
async def root():
    return {"message":"welcome to my api!"}

# @app.get("/sqlalchemy")
# def test_posts( db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}

#response_model=List[schemas.Post]
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    '''
    cursor.execute(""" SELECT * FROM post """)
    posts = cursor.fetchall()
    return {"data": posts}
 
   '''

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=List[schemas.Post])
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):
    #new_post = models.Post(title = post.title,content = post.content,published= post.published)
    
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post
    # cursor.execute("""INSERT INTO post (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    # (
    #     post.title,post.content,post.published
    # ))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data": new_post}
    #post_dict=new_post.dict()
   # post_dict['id']= randrange(0,10000000)
   # my_posts.append(post_dict)
   # return {"new_post" : f"title{payload['title']} content:{payload['content']}"}
   #title str,content str

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"details": post}

@app.get("/posts/{id}")
def get_post(id:int,response: Response,db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM post WHERE id = %s """,(str(id),))
    # post = cursor.fetchone()
    # print(post)
    #post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message':f"post with id:{id} was not found"}
    return {"post details": post}
    #return {"post_detail": f"this is the post {id} ,you were intrested in "}
    
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM post WHERE id = %s RETURNING * """,(str(id),))
    # deleted_post =  cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} dosen't exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post: schemas.PostCreate ,db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE  post SET title = %s, content =%s,published =%s WHERE id = %s RETURNING * """,(
    #     post.title,post.content,post.published,str(id),
    # ))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post=post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id{id} dosen't exist")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {'data': post_query.first()}
#,response_model=schemas.UserOut
@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user