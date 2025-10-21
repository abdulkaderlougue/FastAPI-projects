from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas import UserLogin, UserResponse, Token
from models import User
from database import get_db
import utils
from routers.oauth2 import create_access_token

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm is a dictionary with key username and password
    # need to come as form-data

    user = db.query(User).filter(User.email == user_cred.username).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentials")
    
    if utils.verify_password(user_cred.password, user.password) == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentials")
    
    # token
    access_token = create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    