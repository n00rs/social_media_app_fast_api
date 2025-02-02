
from fastapi import FastAPI,Response,Request,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
import psycopg2
from psycopg2.extras import RealDictCursor
import time

#  create a FastAPI "instance"
app:FastAPI = FastAPI()

# Define a  model for the create post payload
class PostPayload(BaseModel):
    title:str
    content:str
    # optional field with default value
    published: bool = True
    # 
    rating:Optional[int] = None
    int_post_id:Optional[int] = None


while True:
    try:
        #    - *dbname*: the database name
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
# dummy model List
my_posts: List[PostPayload] = [
            {"title": "title 1", "content": "test 1", "published": True, "rating": 2.5,"int_post_id":1},
            {"title": "title 2 ", "content": "test 2", "published": True, "rating": 2.5,"int_post_id":2}
            ]


# request Get method url: "/"
@app.get("/")
def root():
    return {"body":"Hello 1"}

# request Get method url: "/posts"
@app.get("/get_posts")
def get_posts():
    cursor.execute("SELECT * FROM tbl_post")
    my_posts = cursor.fetchall()
    return {"data":my_posts}


# request POST method url : "/create_posts"
@app.post("/create_post",status_code=status.HTTP_201_CREATED)
def create_post(payload:PostPayload):
    print(type(payload))
    
    print(payload.model_dump())
    # insert Query 
    str_query = """
                INSERT INTO tbl_post( vchr_title , vchr_content ,bln_published)
                VALUES (%s,%s,%s) 
                RETURNING *
                """
    cursor.execute(str_query,(payload.title,payload.content,payload.published))
    # get data returned
    new_post = cursor.fetchone()
    conn.commit()
    print(new_post)
    
    # get the max of the id and add one
    # payload.int_post_id = (max(my_posts,key= lambda x: x['int_post_id'])["int_post_id"] or 0) + 1 
    # to convert pydantic model to dictionary use dict method or model_dump
    # my_posts.append(payload.model_dump())
    return { "created_post" : new_post }

# request get method url : "get_post/latest" to get the latest post 
@app.get("/get_post/latest")
def get_latest_post():
    return {"latest_post":my_posts[ len(my_posts) - 1]}

# request get method url : "/get_post/{id}"
'''
get_post function with id as param with integer
'''
@app.get("/get_post/{id}")
def get_post(id: int,res:Response):
    # get data 
    # dict_post = [post for post in my_posts if post["int_post_id"] == id]
    
    str_query = """
                SELECT * FROM tbl_post WHERE int_post_id = %s
                """
    cursor.execute(str_query,(str(id)))
    dict_post = cursor.fetchone()
    
    if not dict_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with id {id} not found")
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {"str_message":f"Post with id {id} not found"}
        
    return { "post_details" : f"Here is the post id {id}", "body" : dict_post }


# request DELETE method url: "/delete_post/{id}"
@app.delete("/delete_post/{id}",status_code=status.HTTP_202_ACCEPTED)
def delete_post(id:int):
    deleted_post = None
    
    # query to remove data from db
    str_query = """
                DELETE FROM tbl_post WHERE int_post_id = %s RETURNING *
                """
    cursor.execute(str_query,(str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    # for i,post in enumerate(my_posts):
    #     print(post)
    #     if post["int_post_id"] == id:
    #         deleted_post = my_posts.pop(i)
    #         print(deleted_post)
    #         break
    print(deleted_post)
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with id {id} not found")
    
    return { "str_message":" successfully deleted ","delete_post":deleted_post}

    # print(my_posts.index({"int_post_id":id}))

#request PUT method url :"/update_post/{id}"
@app.put("/update_post/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_post(id:int,payload:PostPayload,res:Response,):
    print(payload)
    # flag to know that value has been updated
    updated_post = None
    # update query to up date postgres data
    str_query = """
                UPDATE tbl_post
                SET vchr_title = %s,
                    vchr_content = %s,
                    bln_published = %s
                WHERE int_post_id = %s
                RETURNING *
                """
                
    cursor.execute(str_query,(payload.title,payload.content,payload.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    # loop through my post and find the post with id and change it
 
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    return {"body":updated_post}
        
        
