import json
from typing import Optional, List, Dict, Any, cast
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit.types import Pagination, ThreadFilter, ThreadDict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class SQLiteFriendlyDataLayer(SQLAlchemyDataLayer):
    """
    SQLite-compatible data layer that fixes Chainlit's SQLAlchemyDataLayer bug.
    
    The bug: SQLAlchemyDataLayer passes Python lists directly to SQLite for the
    'tags' field, causing sqlite3.InterfaceError since SQLite doesn't support arrays.
    
    Solution: JSON-serialize tags on write, deserialize on read (like metadata field).
    """
    
    def __init__(self, conninfo: str, ssl_require: bool = False, show_logger: bool = False):
        self._conninfo = conninfo
        self.user_thread_limit = 1000
        self.show_logger = show_logger
        self.storage_provider = None
        
        self.engine = create_async_engine(
            self._conninfo,
            pool_size=1,
            max_overflow=0,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={
                "timeout": 30,
                "check_same_thread": False
            }
        )
        
        self.async_session = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )  # type: ignore
    
    async def create_step(self, step_dict):  # type: ignore
        """Override to serialize tags list to JSON string before database insert."""
        step_dict_copy = dict(step_dict)
        if step_dict_copy.get("tags") and isinstance(step_dict_copy["tags"], list):
            step_dict_copy["tags"] = json.dumps(step_dict_copy["tags"])
        
        await super().create_step(step_dict_copy)  # type: ignore
    
    async def update_step(self, step_dict):  # type: ignore
        """Override to serialize tags list to JSON string before database update."""
        step_dict_copy = dict(step_dict)
        if step_dict_copy.get("tags") and isinstance(step_dict_copy["tags"], list):
            step_dict_copy["tags"] = json.dumps(step_dict_copy["tags"])
        
        await super().update_step(step_dict_copy)  # type: ignore
    
    async def update_thread(  # type: ignore
        self,
        thread_id: str,
        name: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
        tags: Optional[Any] = None,
    ):
        """Override to serialize tags list to JSON string before database update."""
        serialized_tags = tags
        if tags is not None and isinstance(tags, list):
            serialized_tags = json.dumps(tags)
        
        await super().update_thread(thread_id, name, user_id, metadata, serialized_tags)  # type: ignore
    
    async def get_thread(self, thread_id: str) -> Optional[ThreadDict]:
        """Override to deserialize JSON tags back to list when reading from database."""
        thread = await super().get_thread(thread_id)
        
        if thread:
            thread = self._deserialize_thread_tags(thread)
        
        return thread
    
    async def list_threads(
        self, pagination: Pagination, filters: ThreadFilter
    ) -> Any:
        """Override to deserialize JSON tags in thread lists."""
        result = await super().list_threads(pagination, filters)
        
        if result and hasattr(result, 'data') and result.data:
            for thread in result.data:
                self._deserialize_thread_tags(thread)
        
        return result
    
    def _deserialize_thread_tags(self, thread: ThreadDict) -> ThreadDict:
        """
        Deserialize JSON tags to Python lists for a thread and its steps.
        
        Args:
            thread: Thread dictionary with potentially serialized tags
            
        Returns:
            Thread dictionary with deserialized tags
        """
        if thread.get("tags") and isinstance(thread["tags"], str):
            try:
                thread["tags"] = json.loads(thread["tags"])
            except (json.JSONDecodeError, TypeError):
                thread["tags"] = []
        
        if thread.get("steps"):
            for step in thread["steps"]:
                if isinstance(step, dict) and step.get("tags") and isinstance(step.get("tags"), str):  # type: ignore
                    try:
                        step["tags"] = json.loads(step["tags"])  # type: ignore
                    except (json.JSONDecodeError, TypeError):
                        step["tags"] = []  # type: ignore
        
        return thread
