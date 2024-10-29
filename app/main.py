from fastapi import  FastAPI, HTTPException,Response,status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating: Optional [int] = None

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

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message":"welcome to my api!"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM post """)
    posts = cursor.fetchall()
    return {"data": posts}
   # return {"data": my_posts}

@app.post("/posts",status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO post (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    (
        post.title,post.content,post.published
    ))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}
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
def get_post(id:int,response: Response):
    cursor.execute(""" SELECT * FROM post WHERE id = %s """,(str(id),))
    post = cursor.fetchone()
    print(post)
    #post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message':f"post with id:{id} was not found"}
    return {"post details": post}
    #return {"post_detail": f"this is the post {id} ,you were intrested in "}
    
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM post WHERE id = %s RETURNING * """,(str(id),))
    deleted_post =  cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} dosen't exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute(""" UPDATE  post SET title = %s, content =%s,published =%s WHERE id = %s RETURNING * """,(
        post.title,post.content,post.published,str(id),
    ))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id{id} dosen't exist")
    return {'data': updated_post}