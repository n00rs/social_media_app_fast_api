from fastapi import status,HTTPException,Depends,APIRouter
import psycopg2
from sqlalchemy.orm import Session
from .. import utils,schemas,model
from ..database import get_db

'''
create router if needed can prefix ie: an /something before route  
eg:prefix= "/posts"
if we want to group by some tag add tags
'''
router = APIRouter(tags= ["user"])
        
#request POST method url: "/create_user"
@router.post("/create_user", status_code= status.HTTP_201_CREATED, response_model=schemas.CreateUserRes)
def create_user(payload: schemas.CreateUserPayload,db: Session = Depends(get_db)):
    try:
        print(payload.model_dump_json())
        # hash the entered user password
        payload.vchr_password = utils.hash(payload.vchr_password)
        
        user = model.User(**payload.model_dump())
        int_add = db.add(user)
        print("int_add",int_add)
        int_add = db.commit()
        print("int_add",int_add)
        
        db.refresh(user)
        # del user.vchr_password
        return { "str_message":"CREATED SUCCEFULLY","body": user }
    except psycopg2.errors.UniqueViolation as err:
        print("UniqueViolation",err)
        raise HTTPException(detail="USER_ALREADY_EXIST",status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        print(err,"errrrr")
        
# request GET method url: "/get_user"
@router.get("/get_user/{int_user_id}", status_code=status.HTTP_200_OK,response_model=schemas.CreateUserRes)
def get_user(int_user_id:int,db:Session = Depends(get_db)):
    try:
        user = db.query(model.User).filter(model.User.int_user_id == int_user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"USER_WITH_{int_user_id}_DOES_NOT_EXIST")
        print(user)
        return {"str_message":"","body": user}
    except Exception as err:
        print(err)
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="")
        raise
