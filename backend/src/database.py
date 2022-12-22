from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.configuration import BaseConfiguration

config = BaseConfiguration()

engine = create_async_engine(
    config.SQLALCHEMY_DATABASE_URL,
    future = True,
    echo = True
)

AsyncSessionFactory = sessionmaker(
    autocommit = False, 
    autoflush = False, 
    bind = engine,
    class_ = AsyncSession
)

Base = declarative_base()