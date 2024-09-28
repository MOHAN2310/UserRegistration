from fastapi import Path
from pydantic import BaseModel


class Users(BaseModel):
    Username: str
    Password: str
    Name: str
    email: str 
    dob: str
    Address: str = None

    class Config:
        from_attributes = True