
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import model
from .database import engine,get_pg_connection
from .routes import posts,users,auth,vote
from .config import settings
# 
model.Base.metadata.create_all(bind=engine)

#  create a FastAPI "instance"
app:FastAPI = FastAPI()
'''
list of allowed origins
'''
origins = ["*"]
app.add_middleware(
    CORSMiddleware,  
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # define which methods can be called 
    allow_headers=["*"], # headers list
    )
# create postgres connection 
cursor = get_pg_connection()
# 
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

# request Get method url: "/"
@app.get("/")
def root():
    return {"body":"Hello 1"}
