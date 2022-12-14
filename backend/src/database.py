from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.configuration import BaseConfiguration

config = BaseConfiguration()

engine = create_engine(config.SQLALCHEMY_DATABASE_URL)

LocalSession = sessionmaker(
    autocommit = False, 
    autoflush = False, 
    bind = engine
)

Base = declarative_base()