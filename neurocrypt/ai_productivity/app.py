from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
from .services.db_service import DatabaseService
from .services.ai_service import AIService
from .utils import generate_uuid, format_datetime, handle_error
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI(
    title="NeuroCrypt AI Productivity",
    description="AI-enhanced productivity features for NeuroCrypt",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
db_service = DatabaseService()
ai_service = AIService()

# Models
class TodoItem(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    priority: Optional[int] = 1
    due_date: Optional[str] = None
    completed: bool = False
    created_at: Optional[str] = None
    ai_suggestions: Optional[List[str]] = Field(default_factory=list, description="AI-generated suggestions for the todo")

class JournalEntry(BaseModel):
    id: Optional[str] = None
    content: str
    mood: Optional[str] = None
    tags: List[str] = []
    created_at: Optional[str] = None
    ai_analysis: Optional[Dict[str, Any]] = Field(default_factory=dict, description="AI analysis of the journal entry")

class Goal(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    target_date: Optional[str] = None
    progress: float = 0.0
    status: str = "active"
    created_at: Optional[str] = None
    ai_suggestions: Optional[Dict[str, Any]] = Field(default_factory=dict, description="AI-generated suggestions for the goal")

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to NeuroCrypt AI Productivity API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Todo endpoints
@app.post("/todos/", response_model=TodoItem)
async def create_todo(todo: TodoItem):
    try:
        # Generate AI suggestions
        suggestions = await ai_service.generate_todo_suggestions(todo.title, todo.description)
        
        # Prepare todo data
        todo_data = todo.dict(exclude={'ai_suggestions'})
        todo_data["id"] = generate_uuid()
        todo_data["created_at"] = format_datetime(datetime.utcnow())
        
        # Create todo in database
        created_todo = await db_service.create_todo(todo_data)
        
        # Add AI suggestions to response
        response_data = TodoItem(**created_todo.__dict__)
        response_data.ai_suggestions = suggestions
        
        return response_data
    except Exception as e:
        raise handle_error(e)

@app.get("/todos/", response_model=List[TodoItem])
async def get_todos():
    try:
        todos = await db_service.get_todos()
        return [TodoItem(**todo.__dict__) for todo in todos]
    except Exception as e:
        raise handle_error(e)

# Journal endpoints
@app.post("/journal/", response_model=JournalEntry)
async def create_journal_entry(entry: JournalEntry):
    try:
        # Analyze journal entry with AI
        analysis = await ai_service.analyze_journal_entry(entry.content)
        
        # Prepare entry data
        entry_data = entry.dict(exclude={'ai_analysis'})
        entry_data["id"] = generate_uuid()
        entry_data["created_at"] = format_datetime(datetime.utcnow())
        
        # Create journal entry in database
        created_entry = await db_service.create_journal_entry(entry_data)
        
        # Add AI analysis to response
        response_data = JournalEntry(**created_entry.__dict__)
        response_data.ai_analysis = analysis
        
        return response_data
    except Exception as e:
        raise handle_error(e)

@app.get("/journal/", response_model=List[JournalEntry])
async def get_journal_entries():
    try:
        entries = await db_service.get_journal_entries()
        return [JournalEntry(**entry.__dict__) for entry in entries]
    except Exception as e:
        raise handle_error(e)

# Goal endpoints
@app.post("/goals/", response_model=Goal)
async def create_goal(goal: Goal):
    try:
        # Generate AI suggestions for goal
        suggestions = await ai_service.suggest_goal_improvements(goal.title, goal.description)
        
        # Prepare goal data
        goal_data = goal.dict(exclude={'ai_suggestions'})
        goal_data["id"] = generate_uuid()
        goal_data["created_at"] = format_datetime(datetime.utcnow())
        
        # Create goal in database
        created_goal = await db_service.create_goal(goal_data)
        
        # Add AI suggestions to response
        response_data = Goal(**created_goal.__dict__)
        response_data.ai_suggestions = suggestions
        
        return response_data
    except Exception as e:
        raise handle_error(e)

@app.get("/goals/", response_model=List[Goal])
async def get_goals():
    try:
        goals = await db_service.get_goals()
        return [Goal(**goal.__dict__) for goal in goals]
    except Exception as e:
        raise handle_error(e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 