from multiprocessing import context
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from random import randrange
from  psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# for i in range(4): # Try to connect to database up to four times:

#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', 
#         user = 'postgres', password = '1234', cursor_factory=RealDictCursor) # Temporary solution to hard code the connection values in code
#         cursor = conn.cursor()
#         print("Database connection was successful.")
#         break # Once a successful connection has been made, break out of the while loop.

#     except Exception as error:
#         print("Connection to database failed")
#         print("Error message: ", error)
#         time.sleep(2) # Wait for 2 seconds after failed attempt to connect to database


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
    return "Hello Fast API 2.0.4"

## uvicorn to start a server
## uvicorn main:app
## uvicorn main:app --reload can be used only when in development.
## @app.get("/"). The get is the method. the "/" is the path. What comes under is the function.


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)): # This will be checked to be integer and not a string.
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) # Against best practices
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Below is a staged input that will be commited with conn.commit()
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published)) # This is a sanitized SQL input. Order of input is important.
    # new_post = cursor.fetchone()
    # conn.commit() # All staged changes need to be commited

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Retrieve and store the created post back into the variable new_post
    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # Add extra comma sign att the end to solve the issue: TypeError: not all arguments converted during string formatting.
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist.")
    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) # No data should be sent back when doing a delete.


# Creating a new path operation
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    # (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} does not exist.")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) # decorator
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password - user.password
    hashed_pw = utils.hash(user.password)
    user.password = hashed_pw # This will update the pydantic user model.
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user