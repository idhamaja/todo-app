import enum

from sqlalchemy import Column, DateTime, Enum, String, Text, func
from sqlalchemy.dialects.mysql import CHAR

from app.database import Base
from app.utils import uuid7


class StatusEnum(str, enum.Enum):
    pending = "pending"
    progress = "progress"
    done = "done"


class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Todo(Base):
    __tablename__ = "todos"

    id = Column(CHAR(36), primary_key=True, default=uuid7)
    title = Column(String(255), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.pending)
    priority = Column(Enum(PriorityEnum), nullable=False, default=PriorityEnum.medium)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
