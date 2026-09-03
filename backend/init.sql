-- Jalankan file ini di MySQL/MariaDB untuk membuat database & tabel awal.
-- Tabel juga otomatis dibuat oleh SQLAlchemy saat backend pertama kali dijalankan,
-- tapi disediakan di sini untuk yang ingin setup manual / review skema.

CREATE DATABASE IF NOT EXISTS todo_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE todo_db;

CREATE TABLE IF NOT EXISTS todos (
    id           CHAR(36) NOT NULL PRIMARY KEY,
    title        VARCHAR(255) NOT NULL,
    status       ENUM('pending','progress','done') NOT NULL DEFAULT 'pending',
    priority     ENUM('low','medium','high') NOT NULL DEFAULT 'medium',
    description  TEXT NULL,
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_created_at (created_at),
    INDEX idx_title (title)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
