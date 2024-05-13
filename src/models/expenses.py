from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from datetime import datetime
from sqlalchemy.orm import relationship
from ..config.database import Base


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=datetime.now())
    description = Column(String(length=250))
    amount = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete='CASCADE'))

    category_expense = relationship("Category", back_populates="expenses")

