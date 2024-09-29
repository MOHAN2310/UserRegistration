import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

load_dotenv('dev.env')

database_url = os.getenv('DATABASE_URL')

engine = create_engine(database_url)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    Username = Column(String, unique=True, index=True)
    Password = Column(String, unique=False, index=True)
    Name= Column(String, unique=False, index=True)
    email = Column(String, unique=True, index=True)
    is_verified = Column(Boolean, default=False)
    dob= Column(String, unique=False, index=True)
    Address= Column(String, unique=False, index=True, nullable=True)
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = "profile"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    secret = Column(String(32), nullable=True)
    # is_verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="profile")
