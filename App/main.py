from multiprocessing import context
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from random import randrange
from  psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .Routers import post, user


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


app.include_router(post.router)
app.include_router(user.router)

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

