from sqlmodel import SQLModel, Field, Column
import sqlalchemy.types as types
from typing import Optional, Dict, Any
from datetime import datetime
import json

class JSONDict(types.TypeDecorator):
    """Custom SQLAlchemy type for storing dicts as JSON strings in SQLite."""
    impl = types.String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value

class ScanRecord(SQLModel, table=True):
    """
    Stores a complete web analysis scan result.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    target_url: str = Field(index=True)
    scan_timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # High-level metrics for quick dashboard display
    urls_found: int = Field(default=0)
    broken_links_count: int = Field(default=0)
    missing_security_headers: int = Field(default=0)
    is_ssl_valid: bool = Field(default=False)
    
    # The full JSON dump of the scan for the detail page
    raw_results: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONDict))
