import jwt
import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import schemas, database, models
from config import settings 

# SECRET_KEY
# 
# load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)

def create_access_token(data: dict):
    payload_to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload_to_encode.update({"exp": expire})
    print("Expire time: ", expire)
    encoded_jwt = jwt.encode(payload_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = str(payload.get("user_id"))

        if id is None:
            raise credentials_exception
        
        token_data= schemas.TokenData(id=id) 
        # return id
    
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    tokenData = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == tokenData.id).first()

    return user