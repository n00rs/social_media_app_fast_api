
from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Optional
from .. import model,schemas,oauth2
from ..database import get_db


'''
create router if needed can prefix ie: an /something before route  
eg:prefix= "/posts"
if we want to group by some tag add tags
'''
router = APIRouter(tags= ["post"])

# request Get method url: "/posts"
@router.get("/get_posts",status_code=status.HTTP_200_OK, response_model= list[schemas.GetPosts])
def get_posts(db: Session = Depends(get_db), 
              current_user = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""
              ):

    # using postgres
    # cursor.execute("SELECT * FROM tbl_post")
    # my_posts = cursor.fetchall()
    '''
    using orm
    sqlalchemy
    '''

    # my_posts = db.query(model.Post).filter(model.Post.int_user_id == current_user.int_user_id).limit(limit).all()
    # my_posts = db.query(model.Post).where(model.Post.vchr_content.ilike(f"%{search.strip()}%")).limit(limit).offset(skip).all()
    
    my_posts = db.query(model.Post,func.count(model.Vote.int_post_id).label("int_votes")).join(
               model.Vote,model.Vote.int_post_id == model.Post.int_post_id,isouter=True).where(
               model.Post.vchr_content.ilike(f"%{search.strip()}%")).group_by(
               model.Post.int_post_id).limit(limit).offset(skip).all()
    
    return  my_posts


# request POST method url : "/create_post"
@router.post("/create_post",status_code=status.HTTP_201_CREATED,response_model= schemas.GetPostRes)
def create_post(payload:schemas.CreatePostPayload,
                db:Session = Depends(get_db)
                ,current_user = Depends(oauth2.get_current_user)
                ):
    # payload.int_user_id = current_user.int_user_id
    '''
    USING POSTGRESSQL library
    '''
    # insert Query 
    # str_query = """
    #             INSERT INTO tbl_post( vchr_title , vchr_content ,bln_published)
    #             VALUES (%s,%s,%s) 
    #             RETURNING *
    #             """
    # cursor.execute(str_query,(payload.title,payload.content,payload.published))
    # # get data returned
    # new_post = cursor.fetchone()
    # conn.commit()
    
    '''
    USING SQLALCHEMY 
    create model the call add method and pass it
    '''
    # new_post = model.Post(vchr_content=payload.content,
    #                       vchr_title=payload.title, 
    #                       bln_published = payload.published)
    new_post = model.Post(**payload.model_dump(),int_user_id = current_user.int_user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
       
    # get the max of the id and add one
    # payload.int_post_id = (max(my_posts,key= lambda x: x['int_post_id'])["int_post_id"] or 0) + 1 
    # to convert pydantic model to dictionary use dict method or model_dump
    # my_posts.append(payload.model_dump())
    return { "str_message":" successfully Created","body":{"Post":new_post,"int_votes":0} }  

# request get method url : "get_post/latest" to get the latest post 
@router.get("/get_post/latest")
def get_latest_post():
    return {"latest_post":{}}

# request get method url : "/get_post/{id}"
'''
get_post function with id as param with integer
'''
@router.get("/get_post/{id}",status_code= status.HTTP_200_OK, response_model= schemas.GetPostRes)
def get_post(id: int,res:Response,db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # get data 
    # dict_post = [post for post in my_posts if post["int_post_id"] == id]
    '''
    USING POSTGRESSQL library
    '''
    # str_query = """
    #             SELECT * FROM tbl_post WHERE int_post_id = %s
    #             """
    # cursor.execute(str_query,(str(id)))
    # dict_post = cursor.fetchone()
    '''
    using orm
    sqlalchemy
    '''
    # dict_post = db.query(model.Post).filter(model.Post.int_post_id == id , model.Post.int_user_id == current_user.int_user_id).first()
    
    dict_post = db.query(model.Post,func.count(model.Vote.int_post_id).label("int_votes")).join(
               model.Vote,model.Vote.int_post_id == model.Post.int_post_id,isouter=True).filter(
               model.Post.int_post_id == id , model.Post.int_user_id == current_user.int_user_id).group_by(
               model.Post.int_post_id).first()
    
    if not dict_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with id {id} not found")
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {"str_message":f"Post with id {id} not found"}
        
    return { "str_message" : f"Here is the post id {id}", "body" : dict_post }


# request DELETE method url: "/delete_post/{id}"
@router.delete("/delete_post/{id}",status_code=status.HTTP_202_ACCEPTED, response_model= schemas.GetPostRes)
def delete_post(id:int, db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    deleted_post = None
    
    ''''
    USING POSTGRESQL directly
    '''
    # query to remove data from db
    # str_query = """
    #             DELETE FROM tbl_post WHERE int_post_id = %s RETURNING *
    #             """
    # cursor.execute(str_query,(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit() 
    '''USING CODE'''
    # for i,post in enumerate(my_posts):
    #     print(post)
    #     if post["int_post_id"] == id:
    #         deleted_post = my_posts.pop(i)
    #         print(deleted_post)
    #         break
    post_query = db.query(model.Post).filter(model.Post.int_post_id == id )
    
    deleted_post = post_query.first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with id {id} not found")
    
    ''' if created user and updating user is different
        then block delete
    '''
    if deleted_post.int_user_id != current_user.int_user_id:
        raise HTTPException(detail=" NOT_AUTHORIZED_TO_PERFORM_REQUEST_ACTION",status_code=status.HTTP_403_FORBIDDEN)
    deleted_post = {
        "int_post_id":deleted_post.int_post_id,
        "vchr_title":deleted_post.vchr_title,
        "vchr_content":deleted_post.vchr_content,
        "bln_published":deleted_post.bln_published,
        "created_at":deleted_post.created_at,
        "int_user_id": current_user.int_user_id
        }
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return { "str_message":" successfully deleted ","body":deleted_post}


#request PUT method url :"/update_post/{id}"
@router.put("/update_post/{id}",status_code=status.HTTP_202_ACCEPTED, response_model= schemas.GetPostRes)
def update_post(id:int, 
                payload:schemas.UpdatePostPayload, res:Response, 
                db:Session = Depends(get_db),
                current_user = Depends(oauth2.get_current_user)):
    # flag to know that value has been updated
    updated_post = None
    ''''
    USING POSTGRESQL directly
    '''
    # update query to up date postgres data
    # str_query = """
    #             UPDATE tbl_post
    #             SET vchr_title = %s,
    #                 vchr_content = %s,
    #                 bln_published = %s
    #             WHERE int_post_id = %s
    #             RETURNING *
    #             """
                
    # cursor.execute(str_query,(payload.title,payload.content,payload.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # loop through my post and find the post with id and change it
    update_query = db.query(model.Post).filter(model.Post.int_post_id == id)
    print("update_query",update_query)
    updated_post = update_query.first()
 
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    
    ''' if created user and updating user is different
        then block update
    '''
    if updated_post.int_user_id != current_user.int_user_id:
        raise HTTPException(detail=" NOT_AUTHORIZED_TO_PERFORM_REQUEST_ACTION",status_code=status.HTTP_403_FORBIDDEN)
    # update_query.update({'vchr_title':payload.vchr_title,'vchr_content':payload.vchr_content},synchronize_session=False)
    # or
    update_query.update(payload.model_dump(),synchronize_session=False)
    
    db.commit()
    return {"str_message":"Updated succefully","body":update_query.first()}
