from copy import copy
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

current = None

def generate_date():
    global current
    if current is None:
        current = datetime.now()
        return current
    else:
        c = copy(current)
        current = None
        return c
class Expense(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: generate_date().isoformat())
    date: Optional[datetime] = Field(default_factory=lambda: generate_date())
    description: Optional[str] = Field(default=None, max_length=250, pattern=r'^[A-Za-z0-9\s]+$')
    amount: float = Field(gt=0.0)
    category: int = Field()