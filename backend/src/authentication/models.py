from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import deferred

from src.database import Base


class UserModel(Base):
    __tablename__ = "users"

    first_name = Column(String(256), nullable = False)
    last_name = Column(String(256), nullable = False)
    email = Column(String(256), nullable = False)
    password = deferred(Column(String, nullable = False))
    confirmed = Column(Boolean, default = False)
    confirmation_hash = Column(String, nullable = True)

