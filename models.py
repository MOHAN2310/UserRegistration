from fastapi import Path 
from pydantic import BaseModel, Field


class Users(BaseModel):
    Username: str
    Password: str = Field(min_length=6)
    Name: str
    email: str 
    dob: str
    Address: str = None

    class Config:
        from_attributes = True

class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)