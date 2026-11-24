from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.user import User
from app.models.post import Post
from app.schemas.post import PostCreate



async def create_post(db:AsyncSession,post_data:PostCreate):
    
    result = await db.execute(
        select(User).where(User.id == post_data.user_id)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        user_id=post_data.user_id
    )

    db.add(new_post)

    await db.commit()

    return new_post