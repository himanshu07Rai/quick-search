from fastapi import APIRouter, HTTPException, Depends, status
from .schema import PostCreateSchema
from .service import PostService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session

router = APIRouter()
post_service = PostService()

@router.post('/')
async def create_post(post: PostCreateSchema, session: AsyncSession = Depends(get_session)):
    new_post =  await post_service.create_post(post, session)
    return new_post