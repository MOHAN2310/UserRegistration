import os
import smtplib
import pyotp
import jwt
import uuid
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import Profile, engine, sessionLocal, User
from models import Users

load_dotenv('dev.env')
passwd_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600

MAIL_USERNAME= os.getenv('MAIL_USERNAME')
MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
MAIL_SERVER=str(os.getenv('MAIL_SERVER'))
MAIL_PORT=int(587)
MAIL_FROM=os.getenv('MAIL_FROM_EMAIL')
MAIL_FROM_NAME="MohanrajB"
JWT_SECRET=os.getenv('JWT_SECRET')
JWT_ALGORITHM=os.getenv('JWT_ALGO')

def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash

async def user_exists(email, session: Session):
    users = session.query(User).all()
    for user in users:
        if user.email == email:
            return True
        return False

async def get_user_by_email(email, session: Session):
    users = session.query(User).all()
    for user in users:
        if email == user.email:
            return user
    return None
    
def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

async def send_email_verify(email: str):
    secret = pyotp.random_base32()
    time_window = 60 * 5
    totp = pyotp.TOTP(s=secret, interval=time_window)
    otp = totp.now()
    try:
        with smtplib.SMTP(MAIL_SERVER[0], port=587) as connection:
            connection.starttls()
            connection.login(
                user=MAIL_FROM[0],
                password=MAIL_PASSWORD[0],
            )
            connection.sendmail(
                from_addr=MAIL_FROM[0],
                to_addrs=email,
                msg=f"Subject:Email Verification OTP\n\nYour OTP for email verification in Trade Replicator is: {otp}",
            )
        print(
            "Please check your email for the OTP to complete your registration.",
        )
        return secret
    except Exception as e:
        print("Exception occured while sending email")

async def create_user(user: Users, session: Session, secret: str):
        user_data = User(
            Username=user.Username,
            Name=user.Name,
            email=user.email,
            dob=user.dob,
            Address=user.Address
        )
        user_data.Password = generate_passwd_hash(user.Password)
        profile = Profile(secret=secret)
        user_data.profile = profile
        session.add(user_data)
        session.commit()
        return user_data

def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4())

    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )

        return token_data

    except jwt.PyJWTError as e:
        print("Exception while decoding the token")
        return None
