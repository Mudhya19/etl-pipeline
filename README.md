# 🏗️ ETL Pipeline — Fashion Studio Data

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-65%20passed-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/Coverage-80%25-brightgreen.svg)]()

> **Submission Dicoding** — Proyek ETL Pipeline yang melakukan web scraping data produk fashion dari [fashion-studio.dicoding.dev](https://fashion-studio.dicoding.dev/), membersihkan data, dan menyimpannya ke dalam repositori data.

---

## 📋 Daftar Isi

- [Deskripsi Proyek](#-deskripsi-proyek)
- [Struktur Proyek](#-struktur-proyek)
- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
- [Menjalankan Pipeline](#-menjalankan-pipeline)
- [Menjalankan Unit Test](#-menjalankan-unit-test)
- [Konfigurasi Repositori Data](#-konfigurasi-repositori-data)
  - [CSV](#1-csv-default)
  - [Google Sheets](#2-google-sheets-opsional)
  - [PostgreSQL](#3-postgresql-opsional)
- [Penjelasan Tahapan ETL](#-penjelasan-tahapan-etl)
- [Hasil Output](#-hasil-output)
- [Teknologi yang Digunakan](#-teknologi-yang-digunakan)

---

## 📖 Deskripsi Proyek

Proyek ini membangun **ETL (Extract, Transform, Load) Pipeline** yang:

1. **Extract** — Melakukan web scraping dari website [Fashion Studio](https://fashion-studio.dicoding.dev/) sebanyak 50 halaman (~1000 data produk).
2. **Transform** — Membersihkan dan mentransformasi data mentah menjadi data bersih (menghapus data invalid, konversi harga ke Rupiah, normalisasi format).
3. **Load** — Menyimpan data bersih ke repositori data: CSV, Google Sheets, dan/atau PostgreSQL.

Pipeline dibangun dengan prinsip **modular code** — setiap tahapan ETL disimpan dalam file Python terpisah dan dilengkapi dengan **error handling** serta **unit testing**.

---

## 📁 Struktur Proyek

```
etl pipeline/
├── tests/                     # Unit tests
│   ├── __init__.py
│   ├── test_extract.py        # Test untuk modul extract (18 test cases)
│   ├── test_transform.py      # Test untuk modul transform (30 test cases)
│   └── test_load.py           # Test untuk modul load (11 test cases)
├── utils/                     # Modul ETL
│   ├── __init__.py
│   ├── extract.py             # Tahapan Extract (web scraping)
│   ├── transform.py           # Tahapan Transform (pembersihan data)
│   └── load.py                # Tahapan Load (penyimpanan data)
├── main.py                    # Orchestrator — menjalankan seluruh pipeline
├── requirements.txt           # Daftar dependencies
├── products.csv               # Output data bersih (hasil pipeline)
├── google-sheets-api.json     # Service account key (jika menggunakan Google Sheets)
└── README.md                  # Dokumentasi proyek (file ini)
```

---

## ⚙️ Prasyarat

Pastikan sistem Anda telah memenuhi prasyarat berikut sebelum menjalankan proyek:

| Prasyarat | Versi Minimum | Cek Versi |
|-----------|--------------|-----------|
| **Python** | 3.10+ | `python --version` |
| **pip** | 21.0+ | `pip --version` |
| **Git** _(opsional)_ | Any | `git --version` |
| **PostgreSQL** _(opsional)_ | 12+ | `psql --version` |

---

## 🚀 Instalasi

### 1. Clone atau Download Proyek

```bash
# Clone dari repository (jika menggunakan Git)
git clone <repository-url>
cd "etl pipeline"

# Atau langsung masuk ke folder proyek
cd "c:\Users\IT\data science\etl pipeline"
```

### 2. (Opsional) Buat Virtual Environment

```bash
# Membuat virtual environment
python -m venv venv

# Aktivasi virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies yang diinstall:**

| Package | Fungsi |
|---------|--------|
| `requests` | HTTP requests untuk web scraping |
| `beautifulsoup4` | Parsing HTML |
| `pandas` | Manipulasi dan analisis data |
| `gspread` | Integrasi Google Sheets API |
| `google-auth` | Autentikasi Google API |
| `sqlalchemy` | ORM untuk koneksi database |
| `psycopg2-binary` | Driver PostgreSQL |
| `pytest` | Framework unit testing |
| `pytest-cov` | Plugin coverage untuk pytest |

---

## ▶️ Menjalankan Pipeline

### Menjalankan Seluruh Pipeline

```bash
python main.py
```

**Output yang diharapkan:**

```
============================================================
TAHAP 1: EXTRACT - Scraping data dari website...
============================================================
Scraping page 1/50...
Scraping page 2/50...
...
Scraping page 50/50...
Total products scraped: 967
Berhasil mengambil 967 data mentah.

============================================================
TAHAP 2: TRANSFORM - Membersihkan data...
============================================================
Data after transformation: 867 rows
Data bersih: 867 baris.

============================================================
TAHAP 3: LOAD - Menyimpan data ke repositori...
============================================================
Data berhasil disimpan ke products.csv (867 baris)

============================================================
ETL Pipeline selesai!
============================================================
Total data tersimpan: 867 baris
Kolom: ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
```

> **Catatan:** Proses scraping 50 halaman memakan waktu sekitar 30–60 detik tergantung koneksi internet.

---

## 🧪 Menjalankan Unit Test

### Menjalankan Semua Test

```bash
python -m pytest tests/ -v
```

### Menjalankan Test dengan Coverage Report

```bash
python -m pytest tests/ --cov=utils --cov-report=term-missing
```

### Menjalankan Test per Modul

```bash
# Test extract saja
python -m pytest tests/test_extract.py -v

# Test transform saja
python -m pytest tests/test_transform.py -v

# Test load saja
python -m pytest tests/test_load.py -v
```

### Hasil Test yang Diharapkan

```
65 passed, 0 failed

Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
utils/__init__.py        0      0   100%
utils/extract.py        59      6    90%
utils/load.py           39      3    92%
utils/transform.py      64     24    62%
--------------------------------------------------
TOTAL                  162     33    80%
```

---

## 🗄️ Konfigurasi Repositori Data

### 1. CSV (Default)

CSV **sudah aktif secara default**. Hasil pipeline otomatis tersimpan ke `products.csv`.

Tidak perlu konfigurasi tambahan.

---

### 2. Google Sheets (Opsional)

Untuk menyimpan data ke Google Sheets, ikuti langkah berikut:

#### a. Buat Service Account di Google Cloud Console

1. Buka [Google Cloud Console](https://console.cloud.google.com/).
2. Buat project baru atau pilih project yang sudah ada.
3. Aktifkan **Google Sheets API** dan **Google Drive API**:
   - Navigasi ke **APIs & Services > Library**.
   - Cari dan aktifkan kedua API tersebut.
4. Buat **Service Account**:
   - Navigasi ke **APIs & Services > Credentials**.
   - Klik **Create Credentials > Service Account**.
   - Isi nama, lalu klik **Done**.
5. Buat **Key** untuk Service Account:
   - Klik service account yang baru dibuat.
   - Tab **Keys > Add Key > Create New Key**.
   - Pilih **JSON**, lalu download.
6. **Rename** file JSON yang di-download menjadi `google-sheets-api.json`.
7. **Pindahkan** file tersebut ke root folder proyek.

#### b. Buat Spreadsheet dan Share

1. Buka [Google Sheets](https://sheets.google.com/).
2. Buat spreadsheet baru (misalnya: `ETL Fashion Products`).
3. Klik **Share** dan tambahkan email service account (tertera di file JSON, field `client_email`) sebagai **Editor**.
4. Set juga **General Access** menjadi **"Anyone with the link" → Editor**.

#### c. Aktifkan di `main.py`

Buka file `main.py` dan **uncomment** baris berikut:

```python
# 3b. Simpan ke Google Sheets (opsional - butuh credentials)
load_to_google_sheets(
    clean_data,
    spreadsheet_name="ETL Fashion Products",
    credentials_file="google-sheets-api.json"
)
```

---

### 3. PostgreSQL (Opsional)

Untuk menyimpan data ke PostgreSQL, ikuti langkah berikut:

#### a. Install dan Jalankan PostgreSQL

1. Download dan install [PostgreSQL](https://www.postgresql.org/download/).
2. Pastikan service PostgreSQL berjalan.

#### b. Buat Database

```sql
-- Login ke PostgreSQL
psql -U postgres

-- Buat database baru
CREATE DATABASE etl_db;

-- Verifikasi
\l
```

#### c. Aktifkan di `main.py`

Buka file `main.py` dan **uncomment** serta sesuaikan baris berikut:

```python
# 3c. Simpan ke PostgreSQL (opsional - butuh database)
load_to_postgresql(
    clean_data,
    table_name="products",
    connection_string="postgresql://postgres:password@localhost:5432/etl_db"
)
```

> **Ganti** `postgres` dengan username Anda, `password` dengan password PostgreSQL Anda, dan `etl_db` dengan nama database yang sudah dibuat.

---

## 📊 Penjelasan Tahapan ETL

### Tahap 1: Extract (`utils/extract.py`)

| Fungsi | Deskripsi |
|--------|-----------|
| `fetch_page(url)` | Mengambil konten HTML dari sebuah URL |
| `parse_products(html)` | Mem-parsing HTML menjadi list dictionary produk |
| `scrape_page(page_number)` | Menggabungkan fetch + parse untuk 1 halaman |
| `scrape_all_pages(start, end)` | Loop scraping seluruh halaman + menambahkan kolom Timestamp |

**Data yang diambil:** Title, Price, Rating, Colors, Size, Gender, Timestamp

**URL Pattern:**
- Halaman 1: `https://fashion-studio.dicoding.dev/`
- Halaman 2–50: `https://fashion-studio.dicoding.dev/page{n}.html`

---

### Tahap 2: Transform (`utils/transform.py`)

| Fungsi | Transformasi | Contoh |
|--------|-------------|--------|
| `clean_price()` | USD → IDR (× Rp16.000) | `"$269.98"` → `4,319,680.0` |
| `clean_rating()` | Ekstrak float dari string | `"Rating: ⭐ 4.9 / 5"` → `4.9` |
| `clean_colors()` | Ekstrak angka | `"3 Colors"` → `3` |
| `clean_size()` | Hapus prefix `"Size: "` | `"Size: M"` → `"M"` |
| `clean_gender()` | Hapus prefix `"Gender: "` | `"Gender: Men"` → `"Men"` |
| `remove_invalid_data()` | Hapus `"Unknown Product"` | Baris dihapus |
| `remove_duplicates()` | Hapus baris duplikat | Baris duplikat dihapus |
| `transform_data()` | Menjalankan seluruh transformasi | Orchestrator |

**Data yang dihapus:**
- Produk dengan Title = `"Unknown Product"`
- Produk dengan Rating = `"Invalid Rating"`
- Baris duplikat
- Baris dengan nilai null

---

### Tahap 3: Load (`utils/load.py`)

| Fungsi | Repositori | Format |
|--------|-----------|--------|
| `load_to_csv()` | File CSV | `products.csv` |
| `load_to_google_sheets()` | Google Sheets | Spreadsheet online |
| `load_to_postgresql()` | PostgreSQL | Tabel database |

---

## 📈 Hasil Output

### Spesifikasi Data Bersih

| Kolom | Tipe Data | Contoh | Keterangan |
|-------|-----------|--------|------------|
| `Title` | `object` (string) | `"T-shirt 2"` | Nama produk |
| `Price` | `float64` | `1,634,400.0` | Harga dalam Rupiah (IDR) |
| `Rating` | `float64` | `3.9` | Rating produk (skala 5) |
| `Colors` | `int64` | `3` | Jumlah variasi warna |
| `Size` | `object` (string) | `"M"` | Ukuran: S, M, L, XL, XXL |
| `Gender` | `object` (string) | `"Women"` | Gender: Men, Women, Unisex |
| `Timestamp` | `object` (string) | `"2026-06-10 16:42:55"` | Waktu ekstraksi data |

### Statistik Data

| Metrik | Nilai |
|--------|-------|
| Total data mentah (sebelum transform) | ~967 |
| Total data bersih (setelah transform) | ~867 |
| Data invalid dihapus | ~100 |
| Null values | 0 |
| Duplikat | 0 |
| Range harga | Rp805.600 – Rp8.794.880 |

---

## 🛠️ Teknologi yang Digunakan

| Kategori | Teknologi |
|----------|-----------|
| **Bahasa** | Python 3.10+ |
| **Web Scraping** | `requests`, `beautifulsoup4` |
| **Data Processing** | `pandas` |
| **Google Sheets** | `gspread`, `google-auth` |
| **Database** | `sqlalchemy`, `psycopg2-binary` |
| **Testing** | `pytest`, `pytest-cov` |

---

## 🔧 Troubleshooting

### Pipeline gagal scraping

```
Error fetching https://fashion-studio.dicoding.dev/: ConnectionError
```

**Solusi:** Pastikan koneksi internet aktif dan website bisa diakses.

### Google Sheets error

```
Error saving to Google Sheets: [Errno 2] No such file or directory
```

**Solusi:** Pastikan file `google-sheets-api.json` ada di root folder proyek.

### PostgreSQL error

```
Error saving to PostgreSQL: OperationalError
```

**Solusi:** Pastikan PostgreSQL berjalan dan connection string di `main.py` sudah benar.

### Test coverage rendah

```bash
# Jalankan dengan report detail
python -m pytest tests/ --cov=utils --cov-report=term-missing
```

**Kolom "Missing"** menunjukkan baris kode yang belum ter-cover oleh test.

---

## 📝 Catatan Submission

- ✅ Kode modular (`extract.py`, `transform.py`, `load.py` terpisah)
- ✅ File `requirements.txt` tersedia
- ✅ Tidak menggunakan Jupyter Notebook (`.ipynb`)
- ✅ Kolom `Timestamp` tersedia (Kriteria 1 — Skilled)
- ✅ Error handling di setiap fungsi (Kriteria 1 — Advanced)
- ✅ Unit test dalam folder `tests/` (Kriteria 3)
- ✅ Test coverage ≥ 80% (Kriteria 3 — Advanced)

---

**Dibuat dengan ❤️ untuk Submission Dicoding**
