from datetime import datetime
from pydantic import BaseModel,EmailStr,Field

class UserCreate(BaseModel):
    name:str=Field(min_length=2,max_length=100)
    email:EmailStr
    age:int=Field(ge=18)
    is_active:bool
    
class UserUpdate(BaseModel):
    name:str|None = Field(default=None,min_length=2,max_length=100)
    email:EmailStr | None=None
    age:int | None = Field(default=None,ge=18)
    
class UserResponse(BaseModel):
    id:int
    name:str
    email:str
    age:int
    is_active:bool
    created_at:datetime