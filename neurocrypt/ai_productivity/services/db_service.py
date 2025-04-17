from typing import List, Optional
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./neurocrypt.db")
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Models
class Todo(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(Integer, default=1)
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(String, primary_key=True)
    content = Column(String, nullable=False)
    mood = Column(String)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Goal(Base):
    __tablename__ = "goals"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    target_date = Column(DateTime)
    progress = Column(Float, default=0.0)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class DatabaseService:
    async def get_db(self):
        async with async_session() as session:
            yield session

    # Todo operations
    async def create_todo(self, todo_data: dict) -> Todo:
        async with async_session() as session:
            todo = Todo(**todo_data)
            session.add(todo)
            await session.commit()
            await session.refresh(todo)
            return todo

    async def get_todos(self, skip: int = 0, limit: int = 100) -> List[Todo]:
        async with async_session() as session:
            result = await session.execute(
                f"SELECT * FROM todos LIMIT {limit} OFFSET {skip}"
            )
            return result.fetchall()

    async def get_todo(self, todo_id: str) -> Optional[Todo]:
        async with async_session() as session:
            result = await session.execute(
                f"SELECT * FROM todos WHERE id = '{todo_id}'"
            )
            return result.first()

    async def update_todo(self, todo_id: str, todo_data: dict) -> Optional[Todo]:
        async with async_session() as session:
            todo = await self.get_todo(todo_id)
            if todo:
                for key, value in todo_data.items():
                    setattr(todo, key, value)
                await session.commit()
                await session.refresh(todo)
            return todo

    async def delete_todo(self, todo_id: str) -> bool:
        async with async_session() as session:
            todo = await self.get_todo(todo_id)
            if todo:
                await session.delete(todo)
                await session.commit()
                return True
            return False

    # Journal operations
    async def create_journal_entry(self, entry_data: dict) -> JournalEntry:
        async with async_session() as session:
            entry = JournalEntry(**entry_data)
            session.add(entry)
            await session.commit()
            await session.refresh(entry)
            return entry

    async def get_journal_entries(self, skip: int = 0, limit: int = 100) -> List[JournalEntry]:
        async with async_session() as session:
            result = await session.execute(
                f"SELECT * FROM journal_entries LIMIT {limit} OFFSET {skip}"
            )
            return result.fetchall()

    async def get_journal_entry(self, entry_id: str) -> Optional[JournalEntry]:
        async with async_session() as session:
            result = await session.execute(
                f"SELECT * FROM journal_entries WHERE id = '{entry_id}'"
            )
            return result.first()

    async def update_journal_entry(self, entry_id: str, entry_data: dict) -> Optional[JournalEntry]:
        async with async_session() as session:
            entry = await self.get_journal_entry(entry_id)
            if entry:
                for key, value in entry_data.items():
                    setattr(entry, key, value)
                await session.commit()
                await session.refresh(entry)
            return entry

    async def delete_journal_entry(self, entry_id: str) -> bool:
        async with async_session() as session:
            entry = await self.get_journal_entry(entry_id)
            if entry:
                await session.delete(entry)
                await session.commit()
                return True
            return False

    # Goal operations
    async def create_goal(self, goal_data: dict) -> Goal:
        async with async_session() as session:
            goal = Goal(**goal_data)
            session.add(goal)
            await session.commit()
            await session.refresh(goal)
            return goal

    async def get_goals(self, skip: int = 0, limit: int = 100) -> List[Goal]:
        async with async_session() as session:
            result = await session.execute(
                f"SELECT * FROM goals LIMIT {limit} OFFSET {skip}"
            )
            return result.fetchall()

    async def get_goal(self, goal_id: str) -> Optional[Goal]:
        async with async_session() as session:
            result = await session.execute(
                f"SELECT * FROM goals WHERE id = '{goal_id}'"
            )
            return result.first()

    async def update_goal(self, goal_id: str, goal_data: dict) -> Optional[Goal]:
        async with async_session() as session:
            goal = await self.get_goal(goal_id)
            if goal:
                for key, value in goal_data.items():
                    setattr(goal, key, value)
                await session.commit()
                await session.refresh(goal)
            return goal

    async def delete_goal(self, goal_id: str) -> bool:
        async with async_session() as session:
            goal = await self.get_goal(goal_id)
            if goal:
                await session.delete(goal)
                await session.commit()
                return True
            return False 