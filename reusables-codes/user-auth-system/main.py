from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from routes import auth_router, user_router
from db import Base, engine
import models

# create the databse tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(router=auth_router)
app.include_router(router=user_router)

@app.get("/")
def root():
    return {"message": "Welcome to the User Authentication System"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=9000)
    
