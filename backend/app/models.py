import uuid
from datetime import date, datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional

class BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_deleted: bool = Field(default=False)

    def to_dict(self):
        return self.model_dump()

class User(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    guid: uuid.UUID = Field(default_factory=uuid.uuid4, index=True, unique=True)
    password: str = Field(max_length=128)
    username: str = Field(max_length=150, unique=True)
    name: str = Field(max_length=150, default="")
    email: str = Field(max_length=254, unique=True)
    last_login: Optional[datetime] = Field(default=None)

    tasks: List["Task"] = Relationship(back_populates="user")

class Task(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    guid: uuid.UUID = Field(default_factory=uuid.uuid4, index=True, unique=True)
    priority: int
    text: str
    completed: bool = Field(default=False)
    posted_at: date

    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="tasks")