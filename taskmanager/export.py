"""Modul ekspor tugas (SENGAJA RENTAN - hanya untuk uji Quality Gate)."""
import subprocess


def export_tasks(filename):
    # Rentan: input pengguna masuk ke shell (command injection)
    cmd = "cat tasks.json > " + filename
    subprocess.call(cmd, shell=True)
