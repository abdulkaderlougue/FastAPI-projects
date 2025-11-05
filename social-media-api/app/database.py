from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings as stgs

# import os
# from dotenv import load_dotenv
# load_dotenv()

# db_name = os.getenv('DB_NAME')
# db_host = os.getenv('DB_HOST')
# db_user = os.getenv('DB_USER')
# db_pass = os.getenv('DB_PASS')

SQLALCHEMY_DB_URL = f'postgresql://{stgs.db_user}:{stgs.db_pass}@{stgs.db_host}/{stgs.db_name}'

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    # every request, create a session and close the connection after
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()