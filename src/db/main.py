from sqlmodel import create_engine
from elasticsearch import AsyncElasticsearch as Elasticsearch
from src.config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

# Create a connection to PostgreSQL
async_engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=False))

# Initialize Elasticsearch client
es = Elasticsearch(
    hosts=["http://localhost:9200"]
)

async def get_session() -> AsyncSession: # type: ignore
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session

async def create_index(index_name):
    # Define the custom settings with edge_ngram
    settings = {
        "settings": {
            "analysis": {
                "tokenizer": {
                    "edge_ngram_tokenizer": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 25,
                        "token_chars": ["letter", "digit"]
                    }
                },
                "analyzer": {
                    "edge_ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "edge_ngram_tokenizer"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "edge_ngram_analyzer"
                },
                "content": {
                    "type": "text",
                    "analyzer": "edge_ngram_analyzer"
                }
            }
        }
    }

    # Check if the index already exists and create it if not
    if not await es.indices.exists(index=index_name):
        await es.indices.create(index=index_name, body=settings)
        print(f"Index {index_name} created.")
    else:
        print(f"Index {index_name} already exists.")