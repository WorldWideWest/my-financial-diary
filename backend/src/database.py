from sqlalchemy import create_engine

from src.configuration import BaseConfiguration

config = BaseConfiguration()

engine = create_engine(config.SQLALCHEMY_DATABASE_URL)