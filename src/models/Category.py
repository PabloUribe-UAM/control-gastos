from pydantic import BaseModel, Field
from typing import Optional


class Category(BaseModel):
    id: Optional[int] = Field(default=0)
    type: str = Field(pattern=r'^((income)|(expense))$')
    name: str = Field(min_length=1, max_length=20, pattern=r'^[A-Za-z\s]+$')
    description: Optional[str] = Field(default=None, max_length=250, pattern=r'^[A-Za-z0-9\s]+$')