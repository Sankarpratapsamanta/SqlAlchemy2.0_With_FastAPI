from pydantic import BaseModel

class ProfileCreate(BaseModel):
    bio:str
    user_id:int
    
class ProfileResponse(BaseModel):
    id:int
    bio:str
    user_id:int