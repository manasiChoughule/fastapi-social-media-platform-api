from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models

#from sqlalchemy.orm import Session

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer


from sqlalchemy.orm import Session
from .database import get_db
from .config import settings

# endpoint for url
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# secret_key
# algorithm
#expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        
        id: str = payload.get("user_id")
        print(id)
        if id is None:
            raise credentials_exception
        print(id)
        token_data = schemas.TokenData(id = id)
        
    except JWTError as e:
        print(e)
        raise credentials_exception
    
    return id
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail = f"Could not validate credentials",
                                          headers = {"WWW-Authenticate": "Bearer"})

    user_id = verify_access_token(token, credentials_exception)    
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    return user
    
    