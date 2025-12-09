from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from contextlib import asynccontextmanager


class User(BaseModel):
    name: str
    email: str
    phone: str
    username: str
    location: str
    password: str

class Login(BaseModel):
    username: str
    password: str

storage = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage["current_id"] = 1
    storage["users"] = []
    yield
    # storage.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def status_page():
    response = {
        "msg": "Welcome! This shows that the API is up and running fine",
        "status_code": 200
    }
    return response


@app.post("/register")
async def register(user: User):
    current_time = datetime.now()
    registered_user = {
        "id": storage["current_id"],
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "username": user.username,
        "location": user.location,
        "password": user.password,
        "created_at": current_time,
        "last_modified_at": current_time
    }
    storage["users"].append(registered_user)
    storage["current_id"] += 1
    response = {
        "msg": "User created successfully",
        "status_code": 201,
        "registered_user": registered_user
    }
    return response


@app.get("/view/{user_id}")
async def view_user(user_id: int):
    users = storage["users"]
    users_filter = list(filter(lambda x: x.get("id") == user_id, users))
    current_user = users_filter[0]
    response = {
        "msg": "User details returned successfully",
        "status_code": 200,
        "user": current_user
    }
    return response

@app.put("/update/{user_id}")
async def update_user_details(user: User,user_id: int):
    users = storage["users"]
    users_filter = list(filter(lambda x: x.get("id") == user_id, users))
    current_user = users_filter[0]
    idx = users.index(current_user)
    current_time = datetime.now()
    updated_user = {
        "id": current_user.get("id"),
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "username": user.username,
        "location": user.location,
        "password": user.password,
        "created_at": current_user.get("created_at"),
        "last_modified_at": current_time
    }
    storage["users"][idx] = updated_user
    response = {
        "msg": "User details updated successfully",
        "status_code": 200,
        "updated_user": updated_user
    }
    return response

@app.post("/login")
async def login_user(login: Login):
    users = storage["users"]
    users_filter = list(filter(lambda x: x.get("username") == login.username and x.get("password") == login.password, users))
    current_user = users_filter[0]
    idx = users.index(current_user)
    current_time = datetime.now()
    logged_in_user = {
        "id": current_user.get("id"),
        "name": current_user.get("name"),
        "email": current_user.get("email"),
        "phone": current_user.get("phone"),
        "username": current_user.get("username"),
        "location": current_user.get("location"),
        "password": current_user.get("password"),
        "created_at": current_user.get("created_at"),
        "last_modified_at": current_user.get("last_modified_at"),
        "last_logged_in_at": current_time
    }
    storage["users"][idx] = logged_in_user
    response = {
        "msg": "User logged in successfully",
        "status_code": 200,
        "logged_in_user": logged_in_user
    }
    return response