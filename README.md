# Todo List API - Idham Irama Permana

REST API Todo List — **backend Python (FastAPI) + MySQL**, **frontend Vue 3 + Tailwind CSS**.

## Struktur Proyek

```
todo-app/
├── backend/            # FastAPI + SQLAlchemy + MySQL
│   ├── app/
│   │   ├── main.py     # Route/endpoint API
│   │   ├── models.py   # Model tabel (SQLAlchemy)
│   │   ├── schemas.py  # Skema validasi request/response (Pydantic)
│   │   ├── crud.py     # Fungsi akses database
│   │   ├── database.py # Koneksi database
│   │   └── utils.py    # Generator UUID v7
│   ├── init.sql        # Skema database (opsional, tabel juga dibuat otomatis)
│   ├── requirements.txt
│   └── .env.example
└── frontend/           # Vue 3 + Vite + Tailwind CSS
    ├── src/
    │   ├── App.vue
    │   ├── api.js
    │   └── components/
    ├── package.json
    └── .env.example
```

## Field Todo

| Field       | Tipe                              |
|-------------|------------------------------------|
| id          | UUID v7 (string, primary key)      |
| title       | varchar(255), wajib diisi          |
| status      | enum: pending, progress, done      |
| priority    | enum: low, medium, high            |
| description | text, opsional                     |
| updated_at  | datetime (auto update)             |
| created_at  | datetime (auto saat insert)        |

## 1. Setup Database (MySQL)

Pastikan MySQL/MariaDB sudah terinstall & berjalan, lalu:

```bash
mysql -u root -p < backend/init.sql
```

Ini akan membuat database `todo_db` beserta tabel `todos`. (Tabel juga akan otomatis dibuat oleh backend saat pertama kali dijalankan jika belum ada, jadi langkah ini opsional.)

## 2. Setup Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env sesuai kredensial MySQL Anda (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

uvicorn app.main:app --reload --port 8000
```

Backend berjalan di `http://localhost:8000`.
Dokumentasi API interaktif otomatis tersedia di `http://localhost:8000/docs` (Swagger UI).

## 3. Setup Frontend

```bash
cd frontend
npm install

cp .env.example .env
# Pastikan VITE_API_BASE_URL sesuai alamat backend, default: http://localhost:8000

npm run dev
```

Frontend berjalan di `http://localhost:5173`.

## Endpoint API

| Method | Endpoint                | Keterangan                                   |
|--------|--------------------------|-----------------------------------------------|
| GET    | `/api/todos`            | List todo — mendukung filter, sort, pagination |
| GET    | `/api/todos/{id}`       | Detail satu todo                              |
| POST   | `/api/todos`            | Tambah satu todo (single insert)              |
| PUT    | `/api/todos/{id}`       | Update todo                                   |
| DELETE | `/api/todos/{id}`       | Hapus todo                                    |
| POST   | `/api/todos/seed`       | Insert data acak, body: `{ "count": 1000 }`   |

### Query parameter `GET /api/todos`

- `search` — cari di title & description
- `status` — filter: `pending` / `progress` / `done`
- `priority` — filter: `low` / `medium` / `high`
- `sort_by` — `title` / `status` / `priority` / `created_at` / `updated_at`
- `sort_order` — `asc` / `desc`
- `page` — nomor halaman (mulai dari 1)
- `page_size` — jumlah data per halaman (maks 100)

Contoh:
```
GET /api/todos?status=pending&priority=high&sort_by=created_at&sort_order=desc&page=1&page_size=10
```

## Validasi yang Diterapkan

**Backend (Pydantic — sumber kebenaran, selalu dijalankan walau request tidak lewat frontend):**
- `title`: wajib diisi, tidak boleh kosong/hanya spasi, maksimal 255 karakter
- `status`: harus salah satu dari `pending`, `progress`, `done`
- `priority`: harus salah satu dari `low`, `medium`, `high`
- `description`: opsional, maksimal 2000 karakter
- `sort_by` & `sort_order`: dibatasi whitelist (mencegah SQL injection lewat nama kolom)
- `page`, `page_size`: harus angka positif, `page_size` maksimal 100
- `count` (seed): antara 1 – 10.000
- ID tidak ditemukan → `404 Not Found`
- Input tidak valid → `422 Unprocessable Entity` dengan pesan spesifik per field

**Frontend (Vue):**
- Validasi realtime saat mengetik/blur pada form (title wajib, batas karakter)
- Menampilkan pesan error per-field
- Menampilkan pesan error dari backend jika ada (mis. saat request langsung ke API tetap divalidasi ulang di server)
- Counter karakter untuk title & description

## Catatan Teknis

- **UUID v7** digenerate manual di `backend/app/utils.py` (time-ordered UUID, index-friendly untuk MySQL, tanpa dependency tambahan).
- **Seed 1000 data acak** menggunakan `bulk_save_objects` per-batch (500 data/batch) agar efisien dan tidak membebani memori/koneksi database.
- CORS sudah dikonfigurasi di backend (`CORS_ORIGINS` di `.env`) agar frontend Vue bisa mengakses API.
