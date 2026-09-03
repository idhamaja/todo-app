"""
Fungsi akses database (CRUD) — dipisah dari route handler agar rapi & mudah ditest.
"""
import random
from typing import Optional, Tuple

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models import PriorityEnum, StatusEnum, Todo
from app.utils import uuid7

# Whitelist kolom yang boleh dipakai untuk sorting -> mencegah SQL injection lewat nama kolom
ALLOWED_SORT_FIELDS = {
    "title": Todo.title,
    "status": Todo.status,
    "priority": Todo.priority,
    "created_at": Todo.created_at,
    "updated_at": Todo.updated_at,
}


def get_todo(db: Session, todo_id: str) -> Optional[Todo]:
    return db.query(Todo).filter(Todo.id == todo_id).first()


def get_todos(
    db: Session,
    search: Optional[str] = None,
    status: Optional[StatusEnum] = None,
    priority: Optional[PriorityEnum] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    page: int = 1,
    page_size: int = 10,
) -> Tuple[list, int]:
    query = db.query(Todo)

    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            Todo.title.ilike(like_pattern) | Todo.description.ilike(like_pattern)
        )

    if status:
        query = query.filter(Todo.status == status)

    if priority:
        query = query.filter(Todo.priority == priority)

    total = query.count()

    sort_column = ALLOWED_SORT_FIELDS.get(sort_by, Todo.created_at)
    order_func = asc if sort_order == "asc" else desc
    query = query.order_by(order_func(sort_column), desc(Todo.id))

    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()

    return items, total


def create_todo(db: Session, todo_data) -> Todo:
    todo = Todo(**todo_data.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def update_todo(db: Session, todo: Todo, todo_data) -> Todo:
    update_dict = todo_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo: Todo) -> None:
    db.delete(todo)
    db.commit()


_SAMPLE_TITLES = [
    "Meeting dengan tim", "Kerjakan laporan bulanan", "Review pull request",
    "Belanja kebutuhan kantor", "Update dokumentasi API", "Perbaiki bug login",
    "Deploy ke production", "Backup database", "Riset kompetitor", "Desain UI baru",
    "Optimasi query database", "Setup CI/CD pipeline", "Training karyawan baru",
    "Audit keamanan sistem", "Rapat evaluasi kuartal", "Perbarui dependensi",
    "Buat unit test", "Konfigurasi server", "Kirim invoice ke klien",
    "Follow up email klien", "Siapkan materi presentasi", "Cek log error server",
]

_SAMPLE_DESCRIPTIONS = [
    None,
    "Deskripsi tugas otomatis untuk keperluan pengujian data.",
    "Perlu koordinasi dengan tim lain sebelum dikerjakan.",
    "Prioritas tinggi, harus selesai sebelum akhir minggu.",
]


def bulk_create_random(db: Session, count: int) -> int:
    """Insert `count` data todo secara acak, dilakukan per-batch agar hemat memori."""
    statuses = list(StatusEnum)
    priorities = list(PriorityEnum)

    batch_size = 500
    inserted = 0
    batch = []

    for i in range(count):
        todo = Todo(
            id=uuid7(),
            title=f"{random.choice(_SAMPLE_TITLES)} #{random.randint(1, 99999)}",
            status=random.choice(statuses),
            priority=random.choice(priorities),
            description=random.choice(_SAMPLE_DESCRIPTIONS),
        )
        batch.append(todo)

        if len(batch) >= batch_size:
            db.bulk_save_objects(batch)
            db.commit()
            inserted += len(batch)
            batch = []

    if batch:
        db.bulk_save_objects(batch)
        db.commit()
        inserted += len(batch)

    return inserted
