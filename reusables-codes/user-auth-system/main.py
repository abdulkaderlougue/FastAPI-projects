from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_router, user_router
from db import Base, engine
import models

# create the databse tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# add cors config
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods= ["GET", "POST", "PUT", "DELETE"], #["*"],
    allow_headers=["*"], # list the exact ones in production
)

app.include_router(router=auth_router)
app.include_router(router=user_router)

@app.get("/")
def root():
    return {"message": "Welcome to the User Authentication System"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=9000)
    
