import os
import asyncio
from celery import Celery
from app.db.session import get_session
from app.db.models import User, Conversation, Message
from sqlmodel import select

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "memread_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

async def _save_chat_log(data: dict):
    # This is a hack to run async code in Celery (which is sync by default)
    # In a real app, use asgiref or a proper async worker setup
    from app.db.session import engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.asyncio import AsyncSession
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # 1. Find or Create User
        api_key = data.get("api_key")
        result = await session.exec(select(User).where(User.api_key == api_key))
        user = result.first()
        
        if not user:
            user = User(email=f"user_{api_key[:5]}@example.com", api_key=api_key)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
        # 2. Create Conversation
        conv = Conversation(
            user_id=user.id,
            provider=data.get("provider"),
            external_id=data.get("thread_id")
        )
        session.add(conv)
        await session.commit()
        await session.refresh(conv)
        
        # 3. Add Messages
        for msg in data.get("messages", []):
            db_msg = Message(
                conversation_id=conv.id,
                role=msg.get("role"),
                content=msg.get("content")
            )
            session.add(db_msg)
            
        await session.commit()
        print(f"Saved conversation {conv.id} for user {user.id}")

@celery_app.task
def process_chat_log(data: dict):
    # Run the async save function in a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_save_chat_log(data))
    loop.close()
    return "Processed"
