#schemas.py
from pydantic import BaseModel,EmailStr
from typing import Optional
from pydantic import conint



class Post(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int 
    title: str
    content: str
    owner_id: int
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse  
    votes: int           
    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    username: str
    email: str
    password: str
class UserResponse(BaseModel):
    id: int 
    username: str
    email: str
    is_active: bool
    
    class Config:
        orm_mode = True
class UserLogin(BaseModel):
    email : EmailStr
    password:str
    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token : str
    token_type : str
class TokenData(BaseModel):
    id : Optional[str] = None




class Vote(BaseModel):
    post_id : int
    dir : conint(le=1) # type: ignore