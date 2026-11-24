from fastapi import APIRouter,Depends,HTTPException,status,Query

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database import get_db

from app.schemas.post import PostCreate,PostResponse

from app.service.post import create_post

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.post("/", response_model=PostResponse)
async def create_new_post(
    post_data: PostCreate,
    db: AsyncSession = Depends(get_db)
):

    return await create_post(db, post_data)