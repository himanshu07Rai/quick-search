from sqlmodel import create_engine
from elasticsearch import Elasticsearch
from src.config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

# Create a connection to PostgreSQL
async_engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=False))

# Initialize Elasticsearch client
es = Elasticsearch(Config.ELASTIC_URL)

async def get_session() -> AsyncSession: # type: ignore
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session
