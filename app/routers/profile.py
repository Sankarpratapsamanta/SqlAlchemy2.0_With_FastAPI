from fastapi import APIRouter,Depends,HTTPException,status,Query

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database import get_db

from app.schemas.profile import ProfileCreate,ProfileResponse

from app.service.profile import create_profile

router=APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.post("/", response_model=ProfileResponse)
async def create_new_profile(
    profile_data: ProfileCreate,
    db: AsyncSession = Depends(get_db)
):

    return await create_profile(db, profile_data)