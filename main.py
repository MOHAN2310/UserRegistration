from fastapi.responses import JSONResponse
import uvicorn
import database
import pyotp
import smtplib
from models import Users, UserLoginModel
from database import engine, sessionLocal, User
from mail import mail, create_message
from utils import get_user_by_email, user_exists, create_user, send_email_verify, verify_password
from errors import UserAlreadyExists, InvalidCredentials

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from typing import Annotated

user_list = []

routes = FastAPI()

database.Base.metadata.create_all(bind=engine)

async def get_db() -> Session:
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@routes.post("/send_mail")
async def send_mail(email: str):
    secret = pyotp.random_base32()
    time_window = 60 * 5
    totp = pyotp.TOTP(s=secret, interval=time_window)
    otp = totp.now()
    # await send_email_verify(email)
    html = f"<h1>Subject:Email Verification OTP\n\nYour OTP for email verification in Trade Replicator is: {otp}</h1>"
    message = create_message(
        recipients=[email],
        subject="Verify your email address",    
        body=html
    )
    await mail.send_message(message)
    return {"message":"Email Sent Sucessfully"}


@routes.get("/users")
async def fetch_users_data(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@routes.post("/signup")
async def register_user(user: Users, db: Session = Depends(get_db)):
    email = user.email
    user_exist = await user_exists(email, db)

    if user_exist:
        print("User has provided an email for a user who exists during sign up.", email)
        raise UserAlreadyExists()

    user_data = await create_user(user=user, session=db)
    return {"message": "User registered successfully!", "user": user_data}


@routes.post("/login")
async def login_users(
    login_data: UserLoginModel, db: Session = Depends(get_db)
):
    email = login_data.email
    password = login_data.password

    user = await get_user_by_email(email, db)

    if user is not None and user.is_verified:
        password_valid = verify_password(password, user.Password)
        if password_valid:
            message = "Login successful"
        else:
            message = "Login failed due to invalid creadentials"

        return JSONResponse(
            content={
                "message": message,
                "user": {"email": user.email,},
            }
        )

    raise InvalidCredentials()


if __name__ == "__main__":
   uvicorn.run("main:routes", host="127.0.0.1", port=8000, reload=True)



