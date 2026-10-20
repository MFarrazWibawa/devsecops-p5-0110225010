"""Antarmuka command-line TaskManager."""
import argparse
import sys

from .service import TaskService
from .storage import JsonStorage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskmanager", description="Aplikasi manajemen tugas sederhana")
    parser.add_argument("--file", default="tasks.json", help="Lokasi file penyimpanan JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Tambah tugas baru")
    p_add.add_argument("title")
    p_add.add_argument("--priority", default="medium")
    p_add.add_argument("--due", default=None, help="Tenggat YYYY-MM-DD")

    p_list = sub.add_parser("list", help="Tampilkan tugas")
    p_list.add_argument("--pending", action="store_true")

    p_done = sub.add_parser("done", help="Tandai tugas selesai")
    p_done.add_argument("id", type=int)

    p_del = sub.add_parser("delete", help="Hapus tugas")
    p_del.add_argument("id", type=int)

    sub.add_parser("stats", help="Statistik tugas")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    service = TaskService(JsonStorage(args.file))
    try:
        if args.command == "add":
            task = service.add(args.title, args.priority, args.due)
            print(f"Tugas #{task.id} ditambahkan: {task.title}")
        elif args.command == "list":
            for t in service.list(only_pending=args.pending):
                mark = "x" if t.done else " "
                print(f"[{mark}] #{t.id} ({t.priority}) {t.title} {t.due_date or ''}".rstrip())
        elif args.command == "done":
            print(f"Tugas #{service.complete(args.id).id} selesai")
        elif args.command == "delete":
            service.delete(args.id)
            print(f"Tugas #{args.id} dihapus")
        elif args.command == "stats":
            for key, value in service.stats().items():
                print(f"{key}: {value}")
    except (ValueError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
