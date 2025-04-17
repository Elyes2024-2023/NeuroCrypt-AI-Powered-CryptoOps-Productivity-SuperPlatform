from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
import uvicorn
from neurocrypt.ai_productivity.services.db_service import DatabaseService, init_db
from neurocrypt.ai_productivity.services.ai_service import AIService
from neurocrypt.utils import generate_uuid, get_current_timestamp

app = FastAPI(title="NeuroCrypt AI Productivity")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
db_service = DatabaseService()
ai_service = AIService()

@app.on_event("startup")
async def startup_event():
    await init_db()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": get_current_timestamp()}

# Todo endpoints
@app.post("/todos/")
async def create_todo(todo_data: dict):
    todo_data["id"] = generate_uuid()
    todo_data["created_at"] = datetime.utcnow()
    todo_data["updated_at"] = datetime.utcnow()
    return await db_service.create_todo(todo_data)

@app.get("/todos/", response_model=List[dict])
async def get_todos(skip: int = 0, limit: int = 100):
    return await db_service.get_todos(skip=skip, limit=limit)

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: str):
    todo = await db_service.get_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: str, todo_data: dict):
    todo_data["updated_at"] = datetime.utcnow()
    todo = await db_service.update_todo(todo_id, todo_data)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    success = await db_service.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"status": "success"}

# Journal endpoints
@app.post("/journal/")
async def create_journal_entry(entry_data: dict):
    entry_data["id"] = generate_uuid()
    entry_data["created_at"] = datetime.utcnow()
    entry_data["updated_at"] = datetime.utcnow()
    return await db_service.create_journal_entry(entry_data)

@app.get("/journal/", response_model=List[dict])
async def get_journal_entries(skip: int = 0, limit: int = 100):
    return await db_service.get_journal_entries(skip=skip, limit=limit)

@app.get("/journal/{entry_id}")
async def get_journal_entry(entry_id: str):
    entry = await db_service.get_journal_entry(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    return entry

@app.put("/journal/{entry_id}")
async def update_journal_entry(entry_id: str, entry_data: dict):
    entry_data["updated_at"] = datetime.utcnow()
    entry = await db_service.update_journal_entry(entry_id, entry_data)
    if entry is None:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    return entry

@app.delete("/journal/{entry_id}")
async def delete_journal_entry(entry_id: str):
    success = await db_service.delete_journal_entry(entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    return {"status": "success"}

# Goal endpoints
@app.post("/goals/")
async def create_goal(goal_data: dict):
    goal_data["id"] = generate_uuid()
    goal_data["created_at"] = datetime.utcnow()
    goal_data["updated_at"] = datetime.utcnow()
    return await db_service.create_goal(goal_data)

@app.get("/goals/", response_model=List[dict])
async def get_goals(skip: int = 0, limit: int = 100):
    return await db_service.get_goals(skip=skip, limit=limit)

@app.get("/goals/{goal_id}")
async def get_goal(goal_id: str):
    goal = await db_service.get_goal(goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

@app.put("/goals/{goal_id}")
async def update_goal(goal_id: str, goal_data: dict):
    goal_data["updated_at"] = datetime.utcnow()
    goal = await db_service.update_goal(goal_id, goal_data)
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

@app.delete("/goals/{goal_id}")
async def delete_goal(goal_id: str):
    success = await db_service.delete_goal(goal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"status": "success"}

# AI-powered endpoints
@app.post("/ai/todo-suggestions")
async def get_todo_suggestions(todo_data: dict):
    return await ai_service.generate_todo_suggestions(todo_data)

@app.post("/ai/journal-analysis")
async def analyze_journal_entry(entry_data: dict):
    return await ai_service.analyze_journal_entry(entry_data)

@app.post("/ai/goal-improvements")
async def suggest_goal_improvements(goal_data: dict):
    return await ai_service.suggest_goal_improvements(goal_data)

@app.get("/ai/productivity-insights")
async def get_productivity_insights():
    return await ai_service.get_productivity_insights()

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 