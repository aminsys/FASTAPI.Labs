from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Defning what a post should look like. Getting validation for free.
# This way we can guarantee that the front end will send the type of data that we want.
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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

## uvicorn to start a server
## uvicorn main:app
## uvicorn main:app --reload can be used only when in development.
## @app.get("/"). The get is the method. the "/" is the path. What comes under is the function.


@app.get("/posts")
def get_posts():
    return {"data":my_posts}


@app.get("/posts/{id}")
def get_post(id: int): # This will be checked to be integer and not a string.
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return {"Post detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED) # Against best practices
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(100, 100000)
    my_posts.append(post_dict)
    return {"New post": f"{post_dict}"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # For deteting a post, find the index for the item
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist.")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) # No data should be sent back when doing a delete.


# Creating a new path operation
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # Find the index of the post with the id:
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} does not exist.")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"Message": post_dict}