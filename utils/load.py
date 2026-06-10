"""
Load module - Menyimpan data ke berbagai repositori.
Mendukung: CSV, Google Sheets, dan PostgreSQL.
"""

import pandas as pd


def load_to_csv(df, filename="products.csv"):
    """
    Menyimpan DataFrame ke file CSV.
    
    Args:
        df (pd.DataFrame): DataFrame yang akan disimpan.
        filename (str): Nama file output (default: products.csv).
    """
    try:
        df.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename} ({len(df)} baris)")
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        raise


def load_to_google_sheets(df, spreadsheet_name, credentials_file):
    """
    Menyimpan DataFrame ke Google Sheets.
    
    Pastikan:
    - File credentials (service account JSON) tersedia.
    - Google Sheets API & Google Drive API sudah diaktifkan.
    - Spreadsheet di-share ke email service account sebagai Editor.
    
    Args:
        df (pd.DataFrame): DataFrame yang akan disimpan.
        spreadsheet_name (str): Nama spreadsheet di Google Sheets.
        credentials_file (str): Path ke file JSON service account.
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = Credentials.from_service_account_file(
            credentials_file, scopes=scopes
        )
        gc = gspread.authorize(credentials)

        # Coba buka spreadsheet, jika tidak ada maka buat baru
        try:
            sh = gc.open(spreadsheet_name)
        except gspread.SpreadsheetNotFound:
            sh = gc.create(spreadsheet_name)
            sh.share("", perm_type="anyone", role="writer")

        worksheet = sh.sheet1
        worksheet.clear()

        # Konversi DataFrame ke list of lists
        header = df.columns.values.tolist()
        values = df.values.tolist()
        data = [header] + values

        worksheet.update(range_name="A1", values=data)
        print(f"Data berhasil disimpan ke Google Sheets: {spreadsheet_name} ({len(df)} baris)")
    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")
        raise


def load_to_postgresql(df, table_name, connection_string):
    """
    Menyimpan DataFrame ke tabel PostgreSQL.
    
    Args:
        df (pd.DataFrame): DataFrame yang akan disimpan.
        table_name (str): Nama tabel di database.
        connection_string (str): Connection string PostgreSQL.
            Contoh: "postgresql://user:password@localhost:5432/database_name"
    """
    try:
        from sqlalchemy import create_engine

        engine = create_engine(connection_string)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"Data berhasil disimpan ke PostgreSQL tabel: {table_name} ({len(df)} baris)")
    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")
        raise
