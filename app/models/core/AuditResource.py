from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

class AuditResource(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    created_by: str
    created_by_user_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    updated_by: Optional[str] = None
    updated_by_user_id: Optional[int] = None
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

    deleted_by: Optional[str] = None
    deleted_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None