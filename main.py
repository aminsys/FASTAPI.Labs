from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

# Defning what a post should look like. Getting validation for free.
# This way we can guarantee that the front end will send the type of data that we want.
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# Route/ path operation
#decorator - without this, this won't be other than a normal python function
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
    return {"data":"This is your posts"}

@app.post("/posts") # Against best practices
def create_posts(new_post: Post):
    print(new_post.rating)
    print(new_post.dict()) # A way to convert the data into a dictionary form.
    return {"New post": f"New post"}