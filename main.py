import database
from models import Users
from database import engine, sessionLocal, User
from mail import mail, create_message

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
    html = "<h1>Welcome to Mera Mentor</h1>"
    message = create_message(
        recipients=[email],
        subject="welcome",
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
    print("user data:",user)
    user_data = User(
        Username=user.Username,
        Password=user.Password,
        Name=user.Name,
        email=user.email,
        dob=user.dob,
        Address=user.Address
    )
    db.add(user_data)
    print("User added sucessfully")
    db.commit()
    db.refresh(user_data)
    print("refresed User data" ,user_data)
    return {"message": "User registered successfully!", "user": user_data}




