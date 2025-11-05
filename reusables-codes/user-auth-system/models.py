from sqlalchemy import Column, Integer, String, Boolean, DateTime, TIMESTAMP, text
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)  
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, server_default=text("(datetime('now'))"))
    updated_at = Column(DateTime, nullable=False, server_default=text("(datetime('now'))"), onupdate=text("(datetime('now'))"))
    # postgresql syntax and mysql 
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # updated_at = Column(DateTime, nullable=False, server_default=text('now()'), onupdate=text('now()'))

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
    