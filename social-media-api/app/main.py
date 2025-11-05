
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import models
from database import engine
from routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

api = FastAPI()

origins = ["*"] # allow all origins
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api.include_router(auth.router)
api.include_router(post.router)
api.include_router(user.router)

@api.get('/')
async def home():
    return {"message": "Welcome to the social media api"}



if __name__ == "__main__":
    uvicorn.run(api)