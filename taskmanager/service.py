"""Logika bisnis manajemen tugas."""
from typing import List, Optional

from .models import Task
from .storage import JsonStorage
from .validators import validate_due_date, validate_priority, validate_title


class TaskService:
    def __init__(self, storage: JsonStorage):
        self.storage = storage

    def add(self, title: str, priority: str = "medium", due_date: Optional[str] = None) -> Task:
        tasks = self.storage.load()
        new_id = max((t.id for t in tasks), default=0) + 1
        task = Task(
            id=new_id,
            title=validate_title(title),
            priority=validate_priority(priority),
            due_date=validate_due_date(due_date),
        )
        tasks.append(task)
        self.storage.save(tasks)
        return task

    def list(self, only_pending: bool = False) -> List[Task]:
        tasks = self.storage.load()
        if only_pending:
            tasks = [t for t in tasks if not t.done]
        order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: (order[t.priority], t.id))

    def complete(self, task_id: int) -> Task:
        tasks = self.storage.load()
        for task in tasks:
            if task.id == task_id:
                task.done = True
                self.storage.save(tasks)
                return task
        raise KeyError(f"Tugas dengan id {task_id} tidak ditemukan")

    def delete(self, task_id: int) -> None:
        tasks = self.storage.load()
        remaining = [t for t in tasks if t.id != task_id]
        if len(remaining) == len(tasks):
            raise KeyError(f"Tugas dengan id {task_id} tidak ditemukan")
        self.storage.save(remaining)

    def stats(self) -> dict:
        tasks = self.storage.load()
        done = sum(1 for t in tasks if t.done)
        return {
            "total": len(tasks),
            "done": done,
            "pending": len(tasks) - done,
            "overdue": sum(1 for t in tasks if t.is_overdue()),
        }
