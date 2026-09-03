"""
Pydantic schemas — semua validasi input/output request divalidasi di sini.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import PriorityEnum, StatusEnum


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Judul todo, wajib diisi")
    status: StatusEnum = Field(default=StatusEnum.pending, description="pending | progress | done")
    priority: PriorityEnum = Field(default=PriorityEnum.medium, description="low | medium | high")
    description: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Title tidak boleh kosong atau hanya berisi spasi")
        return v

    @field_validator("description")
    @classmethod
    def clean_description(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        return v if v else None


class TodoCreate(TodoBase):
    """Payload untuk POST /api/todos (single insert)."""
    pass


class TodoUpdate(BaseModel):
    """Payload untuk PUT /api/todos/{id}. Semua field opsional (partial update)."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    description: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Title tidak boleh kosong atau hanya berisi spasi")
        return v

    @field_validator("description")
    @classmethod
    def clean_description(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        return v if v else None


class TodoResponse(TodoBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime


class PaginatedTodoResponse(BaseModel):
    data: List[TodoResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class SeedRequest(BaseModel):
    count: int = Field(default=1000, ge=1, le=10000, description="Jumlah data acak yang di-generate")


class MessageResponse(BaseModel):
    message: str
