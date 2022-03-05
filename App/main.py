from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Defning what a post should look like. Getting validation for free.
# This way we can guarantee that the front end will send the type of data that we want.
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

for i in range(4): # Try to connect to database up to four times:

    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', 
        user = 'postgres', password = '1234', cursor_factory=RealDictCursor) # Temporary solution to hard code the connection values in code
        cursor = conn.cursor()
        print("Database connection was successful.")
        break # Once a successful connection has been made, break out of the while loop.

    except Exception as error:
        print("Connection to database failed")
        print("Error message: ", error)
        time.sleep(2) # Wait for 2 seconds after failed attempt to connect to database


# Test data saved in memory... until setting up database
my_posts = [{"title": "My first post in the food blog", "content": "This post is a test post for my new accout in food blog", "id": 1},
{"title": "Why pizza is not a healthy choice for teenages", "content": "As vegan, I love pizza, however...", "id": 2}]

# Not a best practice, but will do for now.
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


# For finding a post by index
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# Route/ path operation
# decorator - without this, this won't be other than a normal python function
@app.get("/") # The path that we have to go to. Example: ("/login") to go to login page.

#function
async def root():
    return {"message": "Hello Fast API 2.0.4"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"Status": "Success"}

## uvicorn to start a server
## uvicorn main:app
## uvicorn main:app --reload can be used only when in development.
## @app.get("/"). The get is the method. the "/" is the path. What comes under is the function.


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}


@app.get("/posts/{id}")
def get_post(id: int): # This will be checked to be integer and not a string.
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return {"Post detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED) # Against best practices
def create_posts(post: Post):
    # Below is a staged input that will be commited with conn.commit()
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published)) # This is a sanitized SQL input. Order of input is important.
    new_post = cursor.fetchone()
    conn.commit() # All staged changes need to be commited
    return {"New post": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    # Add extra comma sign att the end to solve the issue: TypeError: not all arguments converted during string formatting.
    cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist.")
    return {deleted_post: Response(status_code=status.HTTP_204_NO_CONTENT)} # No data should be sent back when doing a delete.


# Creating a new path operation
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} does not exist.")

    return {"Message": updated_post}