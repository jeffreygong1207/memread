from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    api_key: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    conversations: List["Conversation"] = Relationship(back_populates="user")
    memories: List["Memory"] = Relationship(back_populates="user")

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    provider: str # openai, anthropic
    external_id: Optional[str] = Field(default=None, index=True) # thread_id from provider
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: User = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    role: str # user, assistant, system
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    conversation: Conversation = Relationship(back_populates="messages")

class Memory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    content: str
    embedding: List[float] = Field(sa_column=Column(Vector(1536))) # OpenAI embedding size
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: User = Relationship(back_populates="memories")
