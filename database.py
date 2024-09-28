from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

URL_DATABASE = 'postgresql://postgres:Security%40123@localhost:5432/user-registration'

engine = create_engine(URL_DATABASE)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    Username = Column(String, unique=True, index=True)
    Password = Column(String, unique=False, index=True)
    Name= Column(String, unique=False, index=True)
    email = Column(String, primary_key=True)
    is_verified = Column(bool, default=False)
    dob= Column(String, unique=False, index=True)
    Address= Column(String, unique=False, index=True, nullable=True)