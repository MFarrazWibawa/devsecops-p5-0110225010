from datetime import date

import pytest

from taskmanager.cli import main
from taskmanager.models import Task
from taskmanager.service import TaskService
from taskmanager.storage import JsonStorage
from taskmanager.validators import validate_due_date, validate_priority, validate_title


@pytest.fixture
def service(tmp_path):
    return TaskService(JsonStorage(str(tmp_path / "t.json")))


def test_add_and_list_sorted_by_priority(service):
    service.add("rendah", "low")
    service.add("tinggi", "high")
    assert [t.title for t in service.list()] == ["tinggi", "rendah"]


def test_complete_and_pending_filter(service):
    t = service.add("a")
    service.add("b")
    service.complete(t.id)
    assert len(service.list(only_pending=True)) == 1


def test_delete_and_not_found(service):
    t = service.add("a")
    service.delete(t.id)
    assert service.list() == []
    with pytest.raises(KeyError):
        service.delete(99)
    with pytest.raises(KeyError):
        service.complete(99)


def test_stats_overdue(service):
    service.add("lama", due_date="2000-01-01")
    s = service.stats()
    assert s["total"] == 1 and s["overdue"] == 1


def test_overdue_logic():
    t = Task(1, "x", due_date="2020-01-01")
    assert t.is_overdue(date(2021, 1, 1))
    t.done = True
    assert not t.is_overdue(date(2021, 1, 1))


def test_validators():
    assert validate_title("  hi ") == "hi"
    with pytest.raises(ValueError):
        validate_title("")
    with pytest.raises(ValueError):
        validate_title("x" * 101)
    with pytest.raises(ValueError):
        validate_priority("urgent")
    assert validate_due_date(None) is None
    with pytest.raises(ValueError):
        validate_due_date("31-12-2025")


def test_cli_flow(tmp_path, capsys):
    f = str(tmp_path / "c.json")
    assert main(["--file", f, "add", "Belajar", "--priority", "high", "--due", "2030-01-01"]) == 0
    assert main(["--file", f, "list"]) == 0
    assert main(["--file", f, "done", "1"]) == 0
    assert main(["--file", f, "stats"]) == 0
    assert main(["--file", f, "delete", "1"]) == 0
    assert main(["--file", f, "done", "1"]) == 1
    assert "Belajar" in capsys.readouterr().out
