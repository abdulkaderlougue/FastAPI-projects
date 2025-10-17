
from typing import List
from fastapi import FastAPI
import uvicorn
import models
from database import engine, get_db
from routers import post, user

models.Base.metadata.create_all(bind=engine)

api = FastAPI()
api.include_router(post.router)
api.include_router(user.router)

@api.get('/')
async def home():
    return {"message": "Welcome to the social media api"}



if __name__ == "__main__":
    uvicorn.run(api)