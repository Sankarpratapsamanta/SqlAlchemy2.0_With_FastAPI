from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.user import User
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate



async def create_profile(db:AsyncSession,profile_data:ProfileCreate):
    
    result = await db.execute(
        select(User).where(User.id == profile_data.user_id)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    new_profile = Profile(
        bio=profile_data.bio,
        user_id=profile_data.user_id
    )

    db.add(new_profile)

    await db.commit()

    return new_profile