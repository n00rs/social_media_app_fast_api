from pydantic import BaseModel,EmailStr,Field
from typing import Optional
from datetime import datetime
from pydantic.types import conint
from typing_extensions import Annotated

# Define a  model for the create post payload
class PostPayloadBase(BaseModel):
    vchr_title:str
    vchr_content:str
    bln_published: bool = True
    # 
    # rating:Optional[int] = None
    # int_post_id:Optional[int] = None

class CreatePostPayload(PostPayloadBase):
    # optional field with default value
    pass

class UpdatePostPayload(PostPayloadBase):
    pass

class CreateUser(BaseModel):
    vchr_email:EmailStr
    int_user_id: int
    created_at: datetime


class PostRes(PostPayloadBase):
    int_post_id:int
    created_at: datetime
    int_user_id: int
    user: CreateUser
    
    class Config:
        from_attributes = True
        
class GetPosts(BaseModel):
    Post:PostRes
    int_votes:int
    
    class Config:
        from_attributes = True

class GetPostRes(BaseModel):
    str_message: str
    body: GetPosts
    
    class Config:
        from_attributes = True

class CreateUserPayload(BaseModel):
    vchr_email : EmailStr
    vchr_password : str



class CreateUserRes(BaseModel):
    str_message: str
    body: CreateUser
    
    class Config:
        from_attributes = True

class LoginRes(BaseModel):
  str_message: str
  str_access_token: str
  token_type: str
  
class TokenPayload(BaseModel):
    int_user_id: int
    
'''
vote payload with the post id 
and dir ie: 1 or 0 
1 for like 
0 for unlike and it should be less than 1
''' 
class Vote(BaseModel):
    int_post_id:int
    dir: Annotated[int,Field(strict=True,le=1)]
    
class VoteRes(BaseModel):
    str_message:str