from sqlalchemy import Column,Integer,PrimaryKeyConstraint,VARCHAR,Boolean,TIMESTAMP,text
from .database import Base

class Post(Base):
    
    __tablename__ = "tbl_post"
    int_post_id = Column(Integer,primary_key=True,nullable=False)
    vchr_content = Column(VARCHAR,nullable=False)
    vchr_title = Column(VARCHAR,nullable=False)
    bln_published = Column(Boolean,server_default='TRUE',nullable=False)
    created_at = Column (TIMESTAMP(timezone=True),server_default= text('now()'),nullable= False)
    
class User(Base):
    __tablename__ = "tbl_user"
    
    int_user_id =  Column(Integer,primary_key=  True,nullable= False)
    vchr_email = Column(VARCHAR,nullable= False,unique= True)
    vchr_password = Column(VARCHAR, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False,server_default= text("now()"))
