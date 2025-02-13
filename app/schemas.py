from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

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

class PostRes(PostPayloadBase):
    int_post_id:int
    created_at: datetime
    
    class Config:
        from_attributes = True

class GetPostRes(BaseModel):
    str_message: str
    body: PostRes
    
    class Config:
        from_attributes = True

class CreateUserPayload(BaseModel):
    vchr_email : EmailStr
    vchr_password : str

class CreateUser(BaseModel):
    vchr_email:EmailStr
    int_user_id: int
    created_at: datetime

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