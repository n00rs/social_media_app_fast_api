
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model
from .database import engine
from .routes import posts,users

# 
model.Base.metadata.create_all(bind=engine)

#  create a FastAPI "instance"
app:FastAPI = FastAPI()

while True:
    try:
        # - *dbname*: the database name
        # - *database*: the database name (only as keyword argument)
        # - *user*: user name used to authenticate
        # - *password*: password used to authenticate
        # - *host*: database host address (defaults to UNIX socket if not provided)
        # - *port*: connection port number (defaults to 5432 if not provided)
        conn = psycopg2.connect("dbname=fastapi user=postgres password=1234 host=172.19.0.1",cursor_factory=RealDictCursor)
        cursor = conn.cursor() 
        print("Database connection succesfull")
        break
    except Exception as err:
        print("Database connection failed")
        print(err)
        time.sleep(2)    

# 
app.include_router(posts.router)
app.include_router(users.router)



# request Get method url: "/"
@app.get("/")
def root():
    return {"body":"Hello 1"}
