from jose import jwt
from datetime import datetime, timedelta, timezone
from config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from db import get_db
from sqlalchemy.orm import Session
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_minutes: int = 15):
    """Create a JWT access token"""

    data_to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes) # time now in UTC + timedelta
    data_to_encode.update({"exp": expire}) # add expiration time to the payload
    jwt_token = jwt.encode(data_to_encode, settings.secret_key, algorithm=settings.algorithm)

    return jwt_token

def verify_access_token(token: str, credentials_exception):
    """ Verify a JWT accesstoken and return the payload data, payload contains the user_id"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        # check if user_id is in the payload
        if payload.get("user_id") is None:
            raise credentials_exception
    # signature invalid or token expired
    except jwt.JWTError:
        raise credentials_exception
    except Exception:
        raise "An error occurred while verifying the token"
    print(payload)
    return payload


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    tokenData = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(tokenData.get('user_id') == User.id).first()
    return user
    
