from fastapi.responses import JSONResponse
import uvicorn
import database
import pyotp
from models import Users, UserLoginModel, UserResponse
from database import engine, sessionLocal, User
from mail import mail, create_message
from utils import create_access_token, decode_token, get_user_by_email, user_exists, create_user, send_email_verify, verify_password
from errors import UserAlreadyExists, InvalidCredentials

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from datetime import timedelta

REFRESH_TOKEN_EXPIRY = 2

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
    html = f"<h1>Email Verification OTP\n\nYour OTP for email verification for user registration is: {otp}</h1>"
    message = create_message(
        recipients=[email],
        subject="Verify your email address",    
        body=html
    )
    await mail.send_message(message)
    return {"message":"Email Sent Sucessfully"}


@routes.post("/verify_mail/{email}/{OTP}")
async def verify_mail(email: str, OTP: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    secret = user.profile.secret
    time_window = 60 * 5
    totp = pyotp.TOTP(s=secret, interval=time_window)

    if totp.verify(OTP):
        user.is_verified = True
        db.add(user)
        db.commit()
        print("Email OTP has been verified succesfully", user.email)
    return {"message":"Verified mail Sucessfully"}


@routes.get("/users")
async def fetch_users_data(db: Session = Depends(get_db)):
    users = db.query(User).all()
    user_data = [UserResponse(
        Username=user.Username,
        email=user.email,
        Name=user.Name,
        dob=user.dob,
        Address=user.Address
    ) for user in users]
    return user_data


@routes.post("/signup")
async def register_user(user: Users, db: Session = Depends(get_db)):
    email = user.email
    user_exist = await user_exists(email, db)

    if user_exist:
        print("User has provided an email for a user who exists during sign up.", email)
        raise UserAlreadyExists()
    
    secret = await send_email_verify(email)
    print("Please check your email for the OTP to complete your registration.", user.email)
    user_data = await create_user(user=user, session=db, secret=secret)
    return {"message": "User registered successfully!", "user": user_data}


@routes.post("/login")
async def login_users(
    login_data: UserLoginModel, db: Session = Depends(get_db)
):
    email = login_data.email
    password = login_data.password
    user = await get_user_by_email(email, db)
    print("Intiating sign in for the user", user.Username)
    if user is not None and user.is_verified:
        password_valid = verify_password(password, user.Password)
        if password_valid:
            print("Sucessfully verified the password for the user", user.Username)
            message = "Login successfull"
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.reference),
                }
            )
            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.reference)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )
        else:
            message = "Login failed due to invalid creadentials"

        return JSONResponse(
            content={
                "message": message,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {"email": user.email, "uid": str(user.reference)},
            }
        )
    raise InvalidCredentials()

@routes.post("/logout")
async def logout(token: str):
    logout_user = decode_token(token=token)
    msg = "Log out failed"
    if logout_user:
        msg = "Logged out successfully"
    return {"msg": msg}


if __name__ == "__main__":
   uvicorn.run("main:routes", host="127.0.0.1", port=8000, reload=True)



