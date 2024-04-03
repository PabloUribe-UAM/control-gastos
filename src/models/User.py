from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(min_length=10, max_length=10, pattern=r'^\d*$')
    email: str = Field(min_length=6, max_length=80, pattern=r'^[a-z0-9!&\-#.~]+@[a-z0-9]+\.(([a-z0-9]+\.)+)?[a-z0-9]+$')
    name: str = Field(min_length=1, max_length=20, pattern=r'^[A-Za-z\s]+$')
    lastname: str = Field(min_length=1, max_length=20, pattern=r'^[A-Za-z\s]+$')
    status: str = Field(pattern=r'^((active)|(inactive))$')