from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import CreateUserPayload,LoginRes
from ..model import User
from ..utils import verify
from ..oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(tags= ["authentication"])

@router.post("/user_login",status_code=status.HTTP_200_OK,response_model= LoginRes)
def user_login(payload:OAuth2PasswordRequestForm = Depends(),db:Session= Depends(get_db)):
    try:
        print(payload)
        user = db.query(User).filter(User.vchr_email == payload.username).first()
        print(user)
        
        if not user or not verify(str_password= payload.password.strip(), str_hashed_password= user.vchr_password):
            raise HTTPException(detail=f"INVALID_CREDENTIAL_{payload.vchr_email}",status_code= status.HTTP_403_FORBIDDEN)
        
        return {"str_message":"LOGIN_SUCCESS",
                "str_access_token" : create_access_token(data={"int_user_id":user.int_user_id}), 
                "token_type": "Bearer" 
                }
    except Exception as err:
        raise err
