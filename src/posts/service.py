from sqlmodel.ext.asyncio.session import AsyncSession
import random
from sqlalchemy.exc import SQLAlchemyError
from .schema import PostSchema, PostCreateSchema
from src.db.models import Post
from src.db.main import es, create_index
from src.utils import SortByEnum
class PostService:
    async def get_posts_by_ids(self, post_ids: list[int], session:AsyncSession) -> list[PostSchema]:
        posts = []
        for post_id in post_ids:
            post = await session.get(Post, post_id)
            if post:
                posts.append(PostSchema.from_orm(post))
        return posts

    async def create_post(self, post:PostCreateSchema, session: AsyncSession) -> PostSchema:
        post_dict = post.model_dump()
        post_dict['likes'] = random.randint(0, 50)
        post_dict['comments'] = random.randint(0, 50)
        new_post = Post(**post_dict)
        try:
            session.add(new_post)
            await session.commit()
            await session.refresh(new_post)
        except SQLAlchemyError as e:
            await session.rollback()
            raise Exception(f"Error creating post: {e}")
        try:
            # create index if not exists
            if not await es.indices.exists(index="posts"):
                await create_index("posts")
            await es.index(
                index="posts",
                id=new_post.id,
                document={"title": new_post.title, "content": new_post.content}
            )
        except Exception as e:
            raise Exception(f"Error indexing post in Elasticsearch: {e}")
        return new_post

    async def search_posts(self, query: str, sort_by:SortByEnum, session: AsyncSession) -> list[PostSchema]:
        try:
            response = await es.search(
                index="posts",
                body={
                    "query": {
                        "multi_match": {
                            "query": query,               # The search term
                            "fields": ["title", "content"], # The fields to search in
                            "fuzziness": "AUTO",           # Optional: to allow fuzzy matching (typos, similar words)
                        }
                    }
                }
            )
            print(response)
            hits = response['hits']['hits']
            post_ids = [hit['_id'] for hit in hits]
            posts = await self.get_posts_by_ids(post_ids, session)
            if sort_by == SortByEnum.likes:
                posts = sorted(posts, key=lambda x: x.likes, reverse=True)
            elif sort_by == SortByEnum.comments:
                posts = sorted(posts, key=lambda x: x.comments, reverse=True)
            return posts
        except Exception as e:
            raise Exception(f"Error searching posts in Elasticsearch: {e}")

