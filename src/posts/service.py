from sqlmodel.ext.asyncio.session import AsyncSession
import random
from .schema import PostSchema, PostCreateSchema
from src.db.models import Post

class PostService:

    def get_post(self, post_id: int, session: AsyncSession) -> PostSchema:
        return self.post_repo.get_post(post_id)

    async def create_post(self, post:PostCreateSchema, session: AsyncSession) -> PostSchema:
        post_dict = post.model_dump()  # Convert Pydantic schema to SQLAlchemy model
        post_dict['likes'] = random.randint(0, 50)
        post_dict['comments'] = random.randint(0, 50)
        new_post = Post(**post_dict)
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)

        # Index post in Elasticsearch
        # await es.index(
        #     index="posts",
        #     id=new_post.id,
        #     document={"title": new_post.title, "content": new_post.content},
        # )
        return new_post

