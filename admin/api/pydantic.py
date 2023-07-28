from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    name:str
    email:str
    phone:str
    password:str
    shopname:str
    gst:int
    is_active: bool = True
    is_active: bool = True
    last_login: datetime
    created_at: datetime
    updated_at: datetime

class Login(BaseModel):
    email : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"