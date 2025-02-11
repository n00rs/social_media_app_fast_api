from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import CreateUserPayload
from ..model import User
from ..utils import verify

router = APIRouter(tags= ["authentication"])

@router.post("/user_login",status_code=status.HTTP_200_OK)
def user_login(payload:CreateUserPayload,db:Session= Depends(get_db)):
    try:
        print(payload)
        user = db.query(User).filter(User.vchr_email == payload.vchr_email).first()
        print(user)
        
        if not user or not verify(str_password= payload.vchr_password.strip(), str_hashed_password= user.vchr_password):
            raise HTTPException(detail=f"INVALID_CREDENTIAL_{payload.vchr_email}",status_code= status.HTTP_404_NOT_FOUND)
        
        return {"str_access_token" : "tets_token"}
    except Exception as err:
        print(err)
