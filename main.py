from fastapi import FastAPI
from models import Users

user_list = []

routes = FastAPI()


@routes.get("/fetchtusers")
async def fetch_users_data():
    return user_list

@routes.post("/registeruser")
async def register_user(user: Users):
    user_list.append(user.dict())
    return user_list




