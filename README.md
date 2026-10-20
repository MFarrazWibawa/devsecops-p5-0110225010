# TaskManager - devsecops-p5-NIM

## 1. Nama Aplikasi & Fungsi
**TaskManager** adalah aplikasi command-line untuk mengelola daftar tugas (to-do):
menambah tugas dengan prioritas dan tenggat, menandai selesai, menghapus, menampilkan
daftar terurut prioritas, serta melihat statistik (total, selesai, tertunda, terlambat).
Data disimpan dalam file JSON lokal.

## 2. Bahasa / Framework
- Python 3.12 (hanya standard library untuk aplikasi)
- pytest + pytest-cov untuk unit test
- Bandit sebagai SAST tool

## 3. Cara Menjalankan
```bash
git clone https://github.com/MFarrazWibawa/devsecops-p5-0110225010.git
cd devsecops-p5-0110225010
pip install -r requirements.txt

python main.py add "Kerjakan laporan" --priority high --due 2026-11-01
python main.py list
python main.py done 1
python main.py stats
python main.py delete 1

# Menjalankan test
pytest --cov=taskmanager
```

## 4. Overview Pipeline CI/CD
Workflow: `.github/workflows/devsecops.yml`, terpicu pada **push** dan **pull_request** ke `main`.

| Job | Fungsi | Quality Gate |
|-----|--------|--------------|
| `build` | Install dependensi & jalankan unit test | Gagal jika test gagal atau coverage < 80% |
| `sast-scan` (`needs: build`) | Analisis statis kode dengan Bandit, laporan JSON di-upload sebagai artifact | Gagal jika ada temuan severity MEDIUM/HIGH |

## Struktur Proyek
```
main.py                 # entry point
taskmanager/            # models, validators, storage, service, cli
tests/test_app.py       # unit test
bandit.yaml             # konfigurasi SAST
.github/workflows/devsecops.yml
```
