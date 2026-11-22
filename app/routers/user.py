from fastapi import APIRouter,Depends,HTTPException,status,Query

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database import get_db

from app.schemas.user import UserCreate,UserUpdate,UserResponse,UserListResponse

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
    
@router.get("/",response_model=UserListResponse)
async def get_users(search:str|None = None,min_age:int|None= Query(default=None,ge=18),max_age:int|None= Query(default=None,ge=18),is_active:bool | None=None,sort_by:str = "id",sort_order:str="asc",page:int=Query(default=1,ge=1),page_size:int=Query(default=10,ge=1,le=100),db:AsyncSession=Depends(get_db)):
    
    if min_age is not None and max_age is not None:
        if min_age > max_age:
            raise HTTPException(status_code=400,detail="min_age cannot be greater than max_age")
        
    if sort_by not in {"id","name","age","created_at"}:
        raise HTTPException(status_code=400,detail="Invalid sort_by")
    
    if sort_order not in {"asc","desc"}:
        raise HTTPException(status_code=400,detail="sort_order must be asc or desc")
    
    
    return await user_service.get_users(db,search,min_age,max_age,is_active,sort_by,sort_order,page,page_size)


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