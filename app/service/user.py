from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate,UserUpdate,UserResponse



async def create_user(db:AsyncSession,user_data:UserCreate):
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        age=user_data.age,
        is_active=user_data.is_active
    )
    
    db.add(new_user)
    
    await db.commit()
    
    return new_user

async def get_users(db:AsyncSession,skip:int=0,limit:int=10):
    users = (select(User).order_by(User.id).offset(skip).limit(limit))
    
    result = await db.scalars(users)
    
    return result.all()

async def get_user(db:AsyncSession,user_id:int):
    return await db.get(User,user_id)

async def update_user(db:AsyncSession,user_id:int,user_data:UserUpdate):
    
    user = await db.get(User,user_id)
    
    if not user:
        return None
    
    update_data = user_data.model_dump(
        exclude_unset=True
    )
    
    for field ,value in update_data.items():
        if field == "email" and value is not None:
            value = str(value)
        setattr(user,field,value)
        
    
    await db.commit()
    
    return user


async def delete_user(db:AsyncSession,user:User):
    await db.delete(user)
    
    await db.commit()
    
    return True
