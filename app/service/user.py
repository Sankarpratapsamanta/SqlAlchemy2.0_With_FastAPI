from sqlalchemy import select,and_,or_,not_,func
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

async def get_users(db:AsyncSession,search:str | None=None,min_age:int | None = None,max_age:int | None = None,is_active:bool | None = None,sort_by:str = "id",sort_order:str = "asc",page:int=0,page_size:int=10):
    # users = (select(User).order_by(User.id).offset(skip).limit(limit))
    
    filters=[]
    
    
    if search:
        search_term = f"%{search}%"
        
        filters.append(
            or_(
                User.name.ilike(search_term),
                User.email.ilike(search_term)
            )
        )
        
    if min_age is not None:
        filters.append(User.age >= min_age)
         
    if max_age is not None:
        filters.append(User.age <= max_age)
        
    if is_active is not None:
        filters.append(User.is_active.is_(is_active))
        
    count_users = (
        select(func.count())
        .select_from(User)
        .where(*filters)
    )
    
    total = await db.scalar(count_users)
    
    users = select(User).where(*filters)
    
    sort_columns={
        "id":User.id,
        "name":User.name,
        "age":User.age,
        "created_at":User.created_at
    }
    
    sort_column = sort_columns.get(sort_by,User.id)
    
    if sort_order == "desc":
        users = users.order_by(sort_column.desc())
    else:
        users = users.order_by(sort_column.asc())
        
    offset = (page - 1) * page_size
    
    users = users.offset(offset).limit(page_size)
    
    result = await db.scalars(users)
    
    return {
        "total":total or 0,
        "page":page,
        "page_size":page_size,
        "items":result.all()
    }
    
    
    
    
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
