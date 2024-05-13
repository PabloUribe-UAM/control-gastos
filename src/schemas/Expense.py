from pydantic import BaseModel, Field
from typing import Optional

class ExpenseSchema(BaseModel):
    description: Optional[str] = Field(default=None, max_length=250, pattern=r'^[A-Za-z0-9\s]+$')
    amount: float = Field(gt=0.0)
    category: int = Field()