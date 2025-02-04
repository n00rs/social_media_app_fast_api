from sqlalchemy import Column,Integer,PrimaryKeyConstraint,VARCHAR,Boolean,TIMESTAMP,text
from .database import Base

class Post(Base):
    
    __tablename__ = "tbl_post"
    int_post_id = Column(Integer,primary_key=True,nullable=False)
    vchr_content = Column(VARCHAR,nullable=False)
    vchr_title = Column(VARCHAR,nullable=False)
    bln_published = Column(Boolean,server_default='TRUE',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default= text('now()'),nullable= False)
    
    