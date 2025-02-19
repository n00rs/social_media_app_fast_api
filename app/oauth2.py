from jwt.exceptions import PyJWTError
import jwt 
from datetime import timedelta,datetime,timezone
from sqlalchemy.orm import Session
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas,database,model,config

ouauth2_scheme = OAuth2PasswordBearer(tokenUrl= "user_login")
#secret key
#Algorithm
#Expriation time
SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expires = datetime.now( timezone.utc ) + expires_delta
    else:
        expires = datetime.now( timezone.utc ) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expires})
    
    str_jwt = jwt.encode(to_encode,key= SECRET_KEY,algorithm=ALGORITHM)
    return str_jwt

def verify_access_token(str_token:str,credentials_exception) -> dict:
    try:
        payload = jwt.decode(str_token,SECRET_KEY,algorithms=[ALGORITHM])
        int_user_id = payload.get("int_user_id")
        if not int_user_id:
            raise credentials_exception
        # get user data from database
        token_data = schemas.TokenPayload(int_user_id= int_user_id)
        return token_data
    except PyJWTError as err:
        print(err)
        raise credentials_exception
    
    except AssertionError as err:
        print(err)
    
def get_current_user(str_token:str = Depends(ouauth2_scheme),db: Session = Depends(database.get_db)):
    # handle exception
    credentials_exception = HTTPException(
                                          status_code= status.HTTP_401_UNAUTHORIZED, 
                                          detail= "could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"},
                                          )
    # verify token and get data 
    token = verify_access_token(str_token,credentials_exception)
    # get user data from db 
    user = db.query(model.User).filter(model.User.int_user_id == token.int_user_id).first()
    return user
    