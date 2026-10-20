"""Modul ekspor tugas (versi aman)."""
import shutil


def export_tasks(filename):
    shutil.copyfile("tasks.json", filename)