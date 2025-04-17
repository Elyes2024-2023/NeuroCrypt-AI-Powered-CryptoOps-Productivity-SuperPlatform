import uuid
from datetime import datetime
from typing import Any, Dict, Optional
import json
from fastapi import HTTPException
import redis
from .config import settings

# Redis client
redis_client = redis.from_url(settings.REDIS_URL) if settings.REDIS_URL else None

def generate_uuid() -> str:
    """Generate a unique identifier."""
    return str(uuid.uuid4())

def get_current_timestamp() -> datetime:
    """Get current UTC timestamp."""
    return datetime.utcnow()

def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO format string."""
    return dt.isoformat()

def parse_datetime(dt_str: str) -> datetime:
    """Parse ISO format string to datetime."""
    return datetime.fromisoformat(dt_str)

def cache_key(prefix: str, identifier: str) -> str:
    """Generate a cache key."""
    return f"{prefix}:{identifier}"

async def get_cached_data(key: str) -> Optional[Any]:
    """Get data from cache."""
    if not redis_client:
        return None
    data = redis_client.get(key)
    return json.loads(data) if data else None

async def set_cached_data(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """Set data in cache."""
    if not redis_client:
        return False
    try:
        redis_client.setex(
            key,
            ttl or settings.CACHE_TTL,
            json.dumps(value)
        )
        return True
    except Exception:
        return False

def validate_json_data(data: Dict[str, Any], required_fields: list) -> bool:
    """Validate JSON data against required fields."""
    return all(field in data for field in required_fields)

def handle_error(error: Exception) -> HTTPException:
    """Handle common errors and return appropriate HTTP exceptions."""
    if isinstance(error, ValueError):
        return HTTPException(status_code=400, detail=str(error))
    elif isinstance(error, KeyError):
        return HTTPException(status_code=400, detail=f"Missing required field: {str(error)}")
    else:
        return HTTPException(status_code=500, detail="Internal server error")

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    # Add more sanitization rules as needed
    return text.strip()

def format_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Format API response."""
    return {
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": format_datetime(get_current_timestamp())
    }

def paginate_results(items: list, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """Paginate a list of items."""
    start = (page - 1) * page_size
    end = start + page_size
    total_items = len(items)
    total_pages = (total_items + page_size - 1) // page_size
    
    return {
        "items": items[start:end],
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    } 