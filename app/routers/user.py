from fastapi import APIRouter,Depends,HTTPException,status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database import get_db

from app.schemas.user import UserCreate,UserUpdate,UserResponse

from app.service import user as user_service

router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(user_data:UserCreate,db:AsyncSession=Depends(get_db)):
    
    try:
        return await user_service.create_user(db,user_data)
    
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User with this email or data already exists")
    
@router.get("/",response_model=list[UserResponse])
async def get_users(skip:int=0,limit:int=10,db:AsyncSession=Depends(get_db)):
    if skip < 0 or limit < 1 or limit > 100:
        raise HTTPException(status_code=400,detail="Invalid pagination")
    return await user_service.get_users(db,skip,limit)


@router.get("/{user_id}",response_model=UserResponse)
async def get_user(user_id:int,db:AsyncSession=Depends(get_db)):
    user = await user_service.get_user(db,user_id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found!")
    
    return user
    
@router.patch("/{user_id}",response_model=UserResponse)
async def update_user(user_id:int,user_data:UserUpdate,db:AsyncSession=Depends(get_db)):
    try:
        return await user_service.update_user(db,user_id,user_data)
    
    except IntegrityError:
        await db.rollback()
        
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already exists!")
    
@router.delete("/{user_id}")
async def delete_user(user_id:int,db:AsyncSession=Depends(get_db)):
    
    user = await user_service.get_user(db,user_id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found!")
    
    await user_service.delete_user(db,user)
    
    return {
        "message":"User deleted successfully!"
    }