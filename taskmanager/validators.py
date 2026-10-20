"""Validasi input pengguna."""
from datetime import date

from .models import PRIORITIES

MAX_TITLE_LENGTH = 100


def validate_title(title: str) -> str:
    title = (title or "").strip()
    if not title:
        raise ValueError("Judul tugas tidak boleh kosong")
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"Judul maksimal {MAX_TITLE_LENGTH} karakter")
    return title


def validate_priority(priority: str) -> str:
    priority = (priority or "").lower()
    if priority not in PRIORITIES:
        raise ValueError(f"Prioritas harus salah satu dari: {', '.join(PRIORITIES)}")
    return priority


def validate_due_date(value):
    if value is None:
        return None
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Format tanggal harus YYYY-MM-DD") from exc
    return value
