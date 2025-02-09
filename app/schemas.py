from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Define a  model for the create post payload
class PostPayloadBase(BaseModel):
    vchr_title:str
    vchr_content:str
    # 
    # rating:Optional[int] = None
    int_post_id:Optional[int] = None

class CreatePostPayload(PostPayloadBase):
    # optional field with default value
    bln_published: bool = True

class UpdatePostPayload(PostPayloadBase):
    pass

class CreatePostResponse(PostPayloadBase):
    int_post_id:int
    bln_published:bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class GetPostRes(BaseModel):
    str_message: str
    body: CreatePostResponse
    
    class Config:
        orm_mode = True
