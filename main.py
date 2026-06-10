"""
Main ETL Pipeline Orchestrator
Menjalankan seluruh proses Extract, Transform, dan Load.
"""

from utils.extract import scrape_all_pages
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql


def main():
    """Menjalankan ETL Pipeline secara berurutan."""

    # =============================================
    # TAHAP 1: EXTRACT
    # =============================================
    print("=" * 60)
    print("TAHAP 1: EXTRACT - Scraping data dari website...")
    print("=" * 60)
    raw_data = scrape_all_pages(start=1, end=50)

    if raw_data.empty:
        print("Gagal mengambil data. Pipeline dihentikan.")
        return

    print(f"Berhasil mengambil {len(raw_data)} data mentah.\n")

    # =============================================
    # TAHAP 2: TRANSFORM
    # =============================================
    print("=" * 60)
    print("TAHAP 2: TRANSFORM - Membersihkan data...")
    print("=" * 60)
    clean_data = transform_data(raw_data)
    print(f"Data bersih: {len(clean_data)} baris.\n")

    # =============================================
    # TAHAP 3: LOAD
    # =============================================
    print("=" * 60)
    print("TAHAP 3: LOAD - Menyimpan data ke repositori...")
    print("=" * 60)

    # 3a. Simpan ke CSV (WAJIB)
    load_to_csv(clean_data, "products.csv")

    # 3b. Simpan ke Google Sheets (opsional - butuh credentials)
    # Uncomment baris di bawah setelah menyiapkan google-sheets-api.json
    # load_to_google_sheets(
    #     clean_data,
    #     spreadsheet_name="ETL Fashion Products",
    #     credentials_file="google-sheets-api.json"
    # )

    # 3c. Simpan ke PostgreSQL (opsional - butuh database)
    # Uncomment baris di bawah setelah menyiapkan PostgreSQL
    # load_to_postgresql(
    #     clean_data,
    #     table_name="products",
    #     connection_string="postgresql://user:password@localhost:5432/etl_db"
    # )

    print("\n" + "=" * 60)
    print("ETL Pipeline selesai!")
    print("=" * 60)
    print(f"Total data tersimpan: {len(clean_data)} baris")
    print(f"Kolom: {list(clean_data.columns)}")
    print(f"\nTipe data:")
    print(clean_data.dtypes)


if __name__ == "__main__":
    main()
