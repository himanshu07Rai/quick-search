import random
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select, SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import desc
from .posts.routes import router as posts_router
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startedssd")
    yield
    print("Application stopped")

app = FastAPI()

version = "v1"

version_prefix =f"/api/{version}"

app.include_router(posts_router, prefix=f"{version_prefix}/posts", tags=["posts"])

# Your existing routes go here
# @app.get("/posts/search/")
# async def search_posts(query: str, sort_by: str = Query("recency", enum=["likes", "comments", "recency"]), session: Session = Depends(get_session)):
#     # Step 1: Search Elasticsearch for matching posts by title or content
#     search_body = {
#         "query": {
#             "multi_match": {
#                 "query": query,
#                 "fields": ["title", "content"],
#                 "type": "phrase_prefix",
#                 "max_expansions": 10
#             }
#         }
#     }
#     response = await es.search(index="posts", body=search_body)
#     post_ids = [int(hit["_id"]) for hit in response["hits"]["hits"]]

#     if not post_ids:
#         return []

#     # Step 2: Fetch posts from PostgreSQL using SQLModel and apply sorting
#     query_stmt = select(Post).where(Post.id.in_(post_ids))

#     if sort_by == "likes":
#         query_stmt = query_stmt.order_by(desc(Post.likes))
#     elif sort_by == "comments":
#         query_stmt = query_stmt.order_by(desc(Post.comments))
#     elif sort_by == "recency":
#         query_stmt = query_stmt.order_by(desc(Post.created_at))

#     posts = session.exec(query_stmt).all()

#     # Step 3: Format the response
#     post_data = [
#         {
#             "id": post.id,
#             "title": post.title,
#             "content": post.content,
#             "likes": post.likes,
#             "comments": post.comments,
#             "created_at": post.created_at
#         }
#         for post in posts
#     ]
#     return post_data

@app.get("/")
async def read_root():
    return {"message": "Welcome to the blog!"}