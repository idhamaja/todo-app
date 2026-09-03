import math
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi import status as http_status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import Base, engine, get_db
from app.models import PriorityEnum, StatusEnum

load_dotenv()

# Membuat tabel otomatis jika belum ada (idempotent, aman dipanggil berkali-kali)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo List API",
    description="REST API Todo List dengan filtering, sorting, pagination, dan seeding data.",
    version="1.0.0",
)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Todo List API is running successfully!"}

@app.get("/api/todos", response_model=schemas.PaginatedTodoResponse, tags=["Todos"])
def list_todos(
    search: Optional[str] = Query(None, max_length=255, description="Cari di title/description"),
    status_filter: Optional[StatusEnum] = Query(None, alias="status"),
    priority: Optional[PriorityEnum] = Query(None),
    sort_by: str = Query(
        "created_at",
        pattern="^(title|status|priority|created_at|updated_at)$",
        description="title | status | priority | created_at | updated_at",
    ),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = crud.get_todos(
        db,
        search=search,
        status=status_filter,
        priority=priority,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )
    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return {
        "data": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


@app.get("/api/todos/{todo_id}", response_model=schemas.TodoResponse, tags=["Todos"])
def get_todo_detail(todo_id: str, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Todo tidak ditemukan")
    return todo


@app.post(
    "/api/todos",
    response_model=schemas.TodoResponse,
    status_code=http_status.HTTP_201_CREATED,
    tags=["Todos"],
)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


@app.put("/api/todos/{todo_id}", response_model=schemas.TodoResponse, tags=["Todos"])
def update_todo_detail(todo_id: str, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    existing = crud.get_todo(db, todo_id)
    if not existing:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Todo tidak ditemukan")
    return crud.update_todo(db, existing, todo)


@app.delete("/api/todos/{todo_id}", response_model=schemas.MessageResponse, tags=["Todos"])
def delete_todo_detail(todo_id: str, db: Session = Depends(get_db)):
    existing = crud.get_todo(db, todo_id)
    if not existing:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Todo tidak ditemukan")
    crud.delete_todo(db, existing)
    return {"message": "Todo berhasil dihapus"}


@app.post("/api/todos/seed", response_model=schemas.MessageResponse, tags=["Todos"])
def seed_todos(payload: schemas.SeedRequest, db: Session = Depends(get_db)):
    inserted = crud.bulk_create_random(db, payload.count)
    return {"message": f"Berhasil menambahkan {inserted} data acak"}
