from sqlalchemy import Enum, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..config.database import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum('income', 'expense'))
    name = Column(String(length=20), unique=True, index=True)
    description = Column(String(length=250))
    user_id = Column(String(length=10), ForeignKey("users.id", ondelete='CASCADE'))

    user = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category_expense")
    incomes = relationship("Income", back_populates="category_income")

