from pydantic import BaseModel, Field
from datetime import date


class Users(BaseModel):
    Username: str
    Password: str = Field(min_length=6)
    Name: str
    email: str 
    dob: date
    Address: str = None

    class Config:
        from_attributes = True

class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

class UserResponse(BaseModel):
    Username: str 
    email: str
    Name: str
    dob: date
    Address: str | None = None 