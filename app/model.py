from sqlalchemy import Column,Integer,PrimaryKeyConstraint,VARCHAR,Boolean,TIMESTAMP,text,ForeignKey
from sqlalchemy.orm import relationship,mapped_column
from .database import Base

class Post(Base):
    
    __tablename__ = "tbl_post"
    int_post_id = Column(Integer,primary_key=True,nullable=False)
    vchr_content = Column(VARCHAR,nullable=False)
    vchr_title = Column(VARCHAR,nullable=False)
    bln_published = Column(Boolean,server_default='TRUE',nullable=False)
    created_at = Column (TIMESTAMP(timezone=True),server_default= text('now()'),nullable= False)
    int_user_id = Column (Integer,ForeignKey(column="tbl_user.int_user_id",ondelete="CASCADE"),nullable=False)
    # managing relationship
    user = relationship("User")
    # vchr_email = mapped_column(ForeignKey("tbl_user.vchr_email"))
class User(Base):
    __tablename__ = "tbl_user"
    
    int_user_id =  Column(Integer,primary_key=  True,nullable= False)
    vchr_email = Column(VARCHAR,nullable= False,unique= True)
    vchr_password = Column(VARCHAR, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False,server_default= text("now()"))

'''
create an table for saving votes 
with voted user id and voted post id
'''
class Vote(Base):
    __tablename__= "tbl_vote"
    
    int_user_id = Column(Integer,ForeignKey(column="tbl_user.int_user_id", ondelete="CASCADE"), primary_key=True)
    int_post_id = Column(Integer,ForeignKey(column="tbl_post.int_post_id", ondelete="CASCADE"), primary_key=True)
    
