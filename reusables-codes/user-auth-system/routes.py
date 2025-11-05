from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import or_
from sqlalchemy.orm import Session
from db import get_db
from models import User
from schemas import UserCreate, UserResponse, UserBase, UserLogin, UserUpdate, TokenData
from utiles.security import hash_password, verify_password
from utiles.jwt import create_access_token, get_current_user

from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/login", response_model=TokenData)
def login(login_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    ''' Login with username or email '''
    # OAuth2PasswordRequestForm has fields username and password, 
    query_user = db.query(User).filter(or_(login_data.username == User.username, login_data.username == User.email))
    user = query_user.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")
    
    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")

    access_token = create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    


# users 
user_router = APIRouter(prefix="/users", tags=["Users"])

# @app.get("/users/me")
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

# protected current user
@user_router.get("/profile", response_model=UserResponse)
def get_profile(current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    ''' Get the current user profile '''
    return current_user

@user_router.get("/", response_model=list[UserResponse])
def get_users(limit=2, skip=0, db: Session = Depends(get_db)):
    ''' Get all users 
    limit: number of user to return
    skip: number of users to skip
    '''
    users = db.query(User).limit(limit).offset(skip).all()
    return users

# protected current user and admin
@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    ''' Get a user by ID '''
    if current_user.id != user_id and current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                      detail="Not allowed to view")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} not found")
    return user


@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    ''' Create a new user '''
    # check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User with this email already exists")
    
    new_user = User(**user.model_dump())
    # hash the password
    new_user.password = hash_password(user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user) # get the newly created user from db
    return new_user

# protected current user and admin
@user_router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UserUpdate, current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    ''' Update a user by ID '''
    # the user can update his profile or 
    # admin 
    # print(current_user.id != user_id)
    if current_user.id != user_id and current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                      detail="Not allowed to update")
        
    query_user = db.query(User).filter(User.id == user_id)
    if not query_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} not found")
    query_user.update(user.model_dump(exclude_unset=True))
    db.commit()
    return query_user.first()

# protected admin
@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    ''' Delete a user by ID '''

    # only admins can delete a user
    if current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                      detail="Not allowed to delete")
    
    query_user = db.query(User).filter(User.id == user_id)
    if not query_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} not found")
    deleted_user = query_user.first()
    query_user.delete(synchronize_session=False)
    db.commit()
    # return {"detail": f"User {user_id} deleted successfully" }


