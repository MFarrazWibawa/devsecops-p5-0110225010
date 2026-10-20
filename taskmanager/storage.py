"""Penyimpanan tugas ke file JSON."""
import json
import os
from typing import List

from .models import Task


class JsonStorage:
    def __init__(self, path: str = "tasks.json"):
        self.path = path

    def load(self) -> List[Task]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            return [Task.from_dict(item) for item in json.load(f)]

    def save(self, tasks: List[Task]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=2, ensure_ascii=False)
