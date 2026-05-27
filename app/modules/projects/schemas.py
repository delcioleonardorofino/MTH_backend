from pydantic import BaseModel
from typing import Any, Dict, Optional
from datetime import datetime
from uuid import UUID


class ProjectCreate(BaseModel):
    title: str
    description: str
    content_json: Dict[str, Any]
    is_published: bool = False

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_json: Optional[Dict[str, Any]]
    is_published: Optional[bool] = None

class ProjectRead(BaseModel):
    id: UUID
    title: str
    description: str
    content_json: Dict[str, Any]
    created_by: UUID
    is_published: bool = False
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime | None

