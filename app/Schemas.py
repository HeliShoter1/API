from pydantic import *
from typing import Optional
from datetime import datetime
from pydantic import conint

#User
class UserBase(BaseModel):
    name : str
    email: EmailStr

class CreateUser(UserBase):
    password : str

class User(UserBase):
    id : int
    create_at : datetime
    class Config:
        from_attributes = True

#Userlogin
class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None  

class PostBase(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None

    def get_dict(self):
        return self.dict()
    
    
class CreatePost(PostBase):
    pass

class Post(PostBase):
    id: int
    create_at: datetime
    id_user : int
    user: User
    
    class Config:
        from_attributes = True


#Vote
class Vote(BaseModel):
    post_id: Optional[int] = None
    dir : conint(le=1)