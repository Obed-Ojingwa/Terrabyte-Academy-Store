from typing import Any, Dict, List, Optional, Union
import uuid
from datetime import datetime


def generate_uuid() -> str:
    """Generate a UUID string"""
    return str(uuid.uuid4())


def get_current_timestamp() -> datetime:
    """Get current timestamp"""
    return datetime.utcnow()


def paginate_query(
    query: Any,
    page: int = 1,
    page_size: int = 20
) -> tuple:
    """
    Apply pagination to a query

    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        page_size: Number of items per page

    Returns:
        Tuple of (paginated_query, total_count)
    """
    # Calculate offset
    offset = (page - 1) * page_size

    # Get total count
    total_count = query.count()

    # Apply pagination
    paginated_query = query.offset(offset).limit(page_size)

    return paginated_query, total_count


def filter_dict(
    data: Dict[str, Any],
    allowed_keys: List[str]
) -> Dict[str, Any]:
    """
    Filter dictionary to only include allowed keys

    Args:
        data: Dictionary to filter
        allowed_keys: List of keys to keep

    Returns:
        Filtered dictionary
    """
    return {k: v for k, v in data.items() if k in allowed_keys}


def is_valid_uuid(val: str) -> bool:
    """Check if a string is a valid UUID"""
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
</parameter