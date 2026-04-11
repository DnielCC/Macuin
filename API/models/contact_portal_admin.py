from __future__ import annotations

from pydantic import BaseModel, Field


class ContactPortalAdminReply(BaseModel):
    admin_reply: str = Field(..., min_length=1, max_length=5000)
