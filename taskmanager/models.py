"""Model data untuk aplikasi TaskManager."""
from dataclasses import dataclass, asdict
from datetime import date
from typing import Optional

PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    done: bool = False
    due_date: Optional[str] = None  # format ISO: YYYY-MM-DD

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            priority=data.get("priority", "medium"),
            done=bool(data.get("done", False)),
            due_date=data.get("due_date"),
        )

    def is_overdue(self, today: Optional[date] = None) -> bool:
        if self.done or not self.due_date:
            return False
        today = today or date.today()
        return date.fromisoformat(self.due_date) < today
