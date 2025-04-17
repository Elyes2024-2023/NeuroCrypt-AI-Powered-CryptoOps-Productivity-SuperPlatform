import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from ..app import app
from ..services.db_service import DatabaseService
from ..services.ai_service import AIService
from ..utils import generate_uuid, format_datetime

client = TestClient(app)

# Test data
test_todo = {
    "id": generate_uuid(),
    "title": "Test Todo",
    "description": "This is a test todo",
    "priority": 1,
    "due_date": format_datetime(datetime.utcnow()),
    "completed": False
}

test_journal = {
    "id": generate_uuid(),
    "content": "This is a test journal entry",
    "mood": "productive",
    "tags": ["test", "development"]
}

test_goal = {
    "id": generate_uuid(),
    "title": "Test Goal",
    "description": "This is a test goal",
    "target_date": format_datetime(datetime.utcnow()),
    "progress": 0.0,
    "status": "active"
}

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_todo():
    response = client.post("/todos/", json=test_todo)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_todo["title"]
    assert data["description"] == test_todo["description"]

def test_get_todos():
    response = client.get("/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_journal_entry():
    response = client.post("/journal/", json=test_journal)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == test_journal["content"]
    assert data["mood"] == test_journal["mood"]

def test_get_journal_entries():
    response = client.get("/journal/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_goal():
    response = client.post("/goals/", json=test_goal)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_goal["title"]
    assert data["description"] == test_goal["description"]

def test_get_goals():
    response = client.get("/goals/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# AI Service Tests
@pytest.mark.asyncio
async def test_generate_todo_suggestions():
    ai_service = AIService()
    suggestions = await ai_service.generate_todo_suggestions(
        "Complete project documentation",
        "Need to write comprehensive docs for the NeuroCrypt project"
    )
    assert isinstance(suggestions, list)
    assert len(suggestions) > 0

@pytest.mark.asyncio
async def test_analyze_journal_entry():
    ai_service = AIService()
    analysis = await ai_service.analyze_journal_entry(
        "Today was a productive day. Completed several tasks and learned new things."
    )
    assert isinstance(analysis, dict)
    assert "mood" in analysis
    assert "themes" in analysis

# Database Service Tests
@pytest.mark.asyncio
async def test_db_operations():
    db_service = DatabaseService()
    
    # Test todo operations
    todo = await db_service.create_todo(test_todo)
    assert todo.title == test_todo["title"]
    
    todos = await db_service.get_todos()
    assert len(todos) > 0
    
    # Test journal operations
    journal = await db_service.create_journal_entry(test_journal)
    assert journal.content == test_journal["content"]
    
    journals = await db_service.get_journal_entries()
    assert len(journals) > 0
    
    # Test goal operations
    goal = await db_service.create_goal(test_goal)
    assert goal.title == test_goal["title"]
    
    goals = await db_service.get_goals()
    assert len(goals) > 0 