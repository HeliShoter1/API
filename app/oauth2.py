from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import *
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .Schemas import *
from . import database, models

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    encode_jwt = jwt.encode(to_encode,SECRET_KET,algorithm=ALGORITHM)
    return encode_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KET, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=str(id))
    except JWTError as e:
        raise credentials_exception
    return token_data

    
def get_current_user(token :str = Depends(oauth_scheme), db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})
    cr_token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == cr_token.id).first()
    return user