import uuid
from http.client import HTTPException
from typing import List
from fastapi import FastAPI, Depends, Response, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from .database import get_db
from .hash_pass import hash, verify


Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)
    username = Column(String)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    login_at = Column(DateTime)

class User(BaseModel):
    name: str
    email: str
    phone: str
    username: str
    location: str
    password: str
    model_config = {"from_attributes": True}

class UserDBTransformer(User):
    id: str
    created_at: datetime
    updated_at: datetime
    login_at: datetime

class RegisterUser(BaseModel):
    registered_user: UserDBTransformer | None
    msg: str
    status_code: int

class UserList(BaseModel):
    users: List[UserDBTransformer]

class ViewUser(BaseModel):
    viewed_user: UserDBTransformer | None
    msg: str
    status_code: int

class UpdateUser(BaseModel):
    updated_user: UserDBTransformer | None
    msg: str
    status_code: int

class Login(BaseModel):
    username: str
    password: str

class LoginUser(BaseModel):
    logged_in_user: UserDBTransformer | None
    msg: str
    status_code: int


app = FastAPI()

@app.get("/")
async def status_page():
    rsp = {
        "msg": "Welcome! This shows that the API is up and running fine",
        "status_code": 200
    }
    return rsp


@app.post("/register", response_model=RegisterUser, status_code=201)
async def register(response:Response, user: User, db: Session = Depends(get_db)):
    user_exists = db.query(UserDB).filter(
        UserDB.username == user.username).first() or db.query(
        UserDB).filter(UserDB.email == user.email).first()
    if user_exists:
        response.status_code = status.HTTP_409_CONFLICT
        rsp = RegisterUser(registered_user=None,
                           msg="User already exists",
                           status_code=409)
        return rsp
    new_id = str(uuid.uuid4())
    current_time = datetime.now()
    hashed_password = hash(user.password)
    registered_user = UserDB(id=new_id, name=user.name,
                email=user.email,
                phone=user.phone, username=user.username,
                location=user.location, password=hashed_password,
                created_at=current_time, updated_at=current_time,
                login_at=current_time)
    db.add(registered_user)
    db.commit()
    db.refresh(registered_user)
    rsp = RegisterUser(registered_user=registered_user,
                            msg="User created successfully",
                            status_code=201)
    return rsp


@app.get("/view/{user_id}", response_model=ViewUser, status_code=200)
async def view_user(response: Response, user_id: str, db: Session = Depends(get_db)):
    users = db.query(UserDB)
    user = users.filter(UserDB.id == user_id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        rsp = ViewUser(viewed_user=None,
                       msg="User does not exist",
                        status_code=404)
        return rsp
    else:
        response.status_code = status.HTTP_200_OK
        rsp = ViewUser(viewed_user=user,
                        msg="User details returned successfully",
                        status_code=200)
        return rsp

@app.put("/update/{user_id}", response_model=UpdateUser, status_code=200)
async def update_user_details(response: Response, user: User,user_id: str, db: Session = Depends(get_db)):
    users = db.query(UserDB)
    user_in_db = users.filter(UserDB.id == user_id).first()
    if not user_in_db:
        response.status_code = status.HTTP_404_NOT_FOUND
        rsp = UpdateUser(updated_user=None,
                         msg="User does not exist",
                           status_code=404)
        return rsp
    current_time = datetime.now()
    for k,v in user:
        setattr(user_in_db, k, v)
    if(user.password):
        hashed_password = hash(user.password)
        user_in_db.password = hashed_password
    user_in_db.updated_at = current_time
    db.commit()
    db.refresh(user_in_db)
    rsp = UpdateUser(updated_user=user_in_db,
                           msg="User details updated successfully",
                           status_code=200)
    return rsp

@app.post("/login", response_model=LoginUser, status_code=200)
async def login_user(response: Response, login: Login, db: Session = Depends(get_db)):
    users = db.query(UserDB)
    user = users.filter(
        UserDB.username == login.username and verify(login.password, UserDB.password)).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        rsp = LoginUser(logged_in_user=None,
                             msg="User does not exist",
                             status_code=404)
        return rsp
    current_time = datetime.now()
    if (verify(login.password, user.password)):
        user.login_at = current_time
        rsp = LoginUser(logged_in_user=user,
                               msg="User logged in successfully",
                               status_code=200)
        return rsp
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        rsp = LoginUser(logged_in_user=None,
                    msg="Please check your login details",
                    status_code=403)
        return rsp