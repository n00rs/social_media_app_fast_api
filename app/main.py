
from fastapi import FastAPI
from . import model
from .database import engine,get_pg_connection
from .routes import posts,users,auth

# 
model.Base.metadata.create_all(bind=engine)

#  create a FastAPI "instance"
app:FastAPI = FastAPI()
# create postgres connection 
cursor = get_pg_connection()
# 
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


# request Get method url: "/"
@app.get("/")
def root():
    return {"body":"Hello 1"}

from os import getenv

pas = getenv("Path")
print(pas)