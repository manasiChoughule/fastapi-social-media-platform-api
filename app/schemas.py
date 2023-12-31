# the file defines all the expected data formats

from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime 

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    
class PostCreate(PostBase):
    pass


        
class UserCreate(BaseModel):
    email : EmailStr
    password : str
    
class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
    class Config:
        orm_mode = True

class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut
    
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: int

    @validator('dir')
    def must_be_one_or_zero(cls, value):
        if value not in (0, 1):
            raise ValueError("Must be either 1 or 0")
        return value


class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True