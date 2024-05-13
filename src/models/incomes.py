from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from datetime import datetime
from sqlalchemy.orm import relationship
from ..config.database import Base


class Income(Base):
    __tablename__ = "incomes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=datetime.now())
    description = Column(String(length=250))
    amount = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete='CASCADE'))

    category_income = relationship("Category", back_populates="incomes")

