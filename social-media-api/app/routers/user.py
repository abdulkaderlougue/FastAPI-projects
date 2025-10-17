import models, schemas, utils
from fastapi import Response, status, HTTPException, Depends, APIRouter
from schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
from typing import List
from database import get_db

router = APIRouter()

@router.get('/users', response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/users/{id}', response_model=UserResponse)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id)

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} was not found")
    return user

@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user