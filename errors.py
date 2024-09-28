from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError

class UserException(Exception):
    """This is the base class for all the errors"""
    pass

class UserAlreadyExists(Exception):
    """User has provided an email for a user who exists during sign up."""
     
class InvalidCredentials(Exception):
    """User has provided wrong email or password during log in."""
    pass