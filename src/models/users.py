from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from src.config.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String(length=10), primary_key=True)
    email = Column(String(length=80), unique=True, index=True)
    name = Column(String(length=20))
    lastname = Column(String(length=20))
    password = Column(String(length=255))
    active = Column(Boolean)

    categories = relationship("Category", back_populates="user")