from pydantic import BaseModel
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
