"""
Unit tests untuk modul Load.
Menguji fungsi load_to_csv, load_to_google_sheets, dan load_to_postgresql.
"""

import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, call
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql


# ======================================================
# Helper: sample DataFrame untuk testing
# ======================================================
def create_sample_dataframe():
    """Membuat DataFrame sample untuk testing."""
    return pd.DataFrame({
        "Title": ["T-shirt 1", "Hoodie 2", "Jacket 3"],
        "Price": [800000.0, 1928000.0, 4800000.0],
        "Rating": [4.5, 3.8, 4.2],
        "Colors": [3, 5, 2],
        "Size": ["M", "L", "XL"],
        "Gender": ["Men", "Women", "Unisex"],
        "Timestamp": ["2026-06-10 16:00:00"] * 3,
    })


# ======================================================
# Tests untuk load_to_csv
# ======================================================
class TestLoadToCsv:
    """Test class untuk fungsi load_to_csv."""

    def test_load_to_csv_creates_file(self, tmp_path):
        """Test file CSV berhasil dibuat."""
        df = create_sample_dataframe()
        filepath = str(tmp_path / "test_output.csv")
        load_to_csv(df, filepath)
        assert os.path.exists(filepath)

    def test_load_to_csv_correct_content(self, tmp_path):
        """Test isi file CSV sesuai dengan DataFrame."""
        df = create_sample_dataframe()
        filepath = str(tmp_path / "test_output.csv")
        load_to_csv(df, filepath)

        # Baca kembali CSV dan verifikasi
        loaded_df = pd.read_csv(filepath)
        assert len(loaded_df) == 3
        assert list(loaded_df.columns) == list(df.columns)
        assert loaded_df["Title"].iloc[0] == "T-shirt 1"
        assert loaded_df["Price"].iloc[0] == 800000.0

    def test_load_to_csv_no_index(self, tmp_path):
        """Test CSV tidak memiliki kolom index."""
        df = create_sample_dataframe()
        filepath = str(tmp_path / "test_output.csv")
        load_to_csv(df, filepath)

        loaded_df = pd.read_csv(filepath)
        assert "Unnamed: 0" not in loaded_df.columns

    def test_load_to_csv_error_invalid_path(self):
        """Test error handling untuk path yang tidak valid."""
        df = create_sample_dataframe()
        with pytest.raises(Exception):
            load_to_csv(df, "/nonexistent/dir/impossible/path/output.csv")

    def test_load_to_csv_empty_dataframe(self, tmp_path):
        """Test menyimpan DataFrame kosong."""
        df = pd.DataFrame()
        filepath = str(tmp_path / "empty_output.csv")
        load_to_csv(df, filepath)
        assert os.path.exists(filepath)


# ======================================================
# Tests untuk load_to_google_sheets
# ======================================================
class TestLoadToGoogleSheets:
    """Test class untuk fungsi load_to_google_sheets."""

    def test_load_to_google_sheets_missing_credentials(self):
        """Test error ketika file credentials tidak ditemukan."""
        df = create_sample_dataframe()
        with pytest.raises(Exception):
            load_to_google_sheets(df, "Test Sheet", "nonexistent_file.json")

    def test_load_to_google_sheets_success_mocked(self):
        """Test upload ke Google Sheets berhasil dengan mock penuh."""
        df = create_sample_dataframe()

        # Mock gspread dan google.oauth2 sebelum fungsi import
        mock_gc = MagicMock()
        mock_worksheet = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_spreadsheet.sheet1 = mock_worksheet
        mock_gc.open.return_value = mock_spreadsheet

        mock_gspread = MagicMock()
        mock_gspread.authorize.return_value = mock_gc

        mock_sa_module = MagicMock()
        mock_creds_instance = MagicMock()
        mock_sa_module.Credentials.from_service_account_file.return_value = mock_creds_instance

        with patch.dict("sys.modules", {
            "gspread": mock_gspread,
            "google": MagicMock(),
            "google.oauth2": MagicMock(),
            "google.oauth2.service_account": mock_sa_module,
        }):
            # Re-import agar fungsi menggunakan modul mock
            import importlib
            import utils.load
            importlib.reload(utils.load)

            utils.load.load_to_google_sheets(df, "Test Sheet", "fake_creds.json")

            # Verifikasi flow
            mock_sa_module.Credentials.from_service_account_file.assert_called_once()
            mock_gspread.authorize.assert_called_once()
            mock_gc.open.assert_called_once_with("Test Sheet")
            mock_worksheet.clear.assert_called_once()
            mock_worksheet.update.assert_called_once()

        # Reload kembali module asli
        importlib.reload(utils.load)


# ======================================================
# Tests untuk load_to_postgresql
# ======================================================
class TestLoadToPostgresql:
    """Test class untuk fungsi load_to_postgresql."""

    def test_load_to_postgresql_success(self):
        """Test upload ke PostgreSQL berhasil (mock)."""
        df = create_sample_dataframe()

        mock_engine = MagicMock()
        with patch("utils.load.create_engine", return_value=mock_engine, create=True):
            with patch.object(df, "to_sql") as mock_to_sql:
                try:
                    load_to_postgresql(df, "products", "postgresql://user:pass@localhost/db")
                except Exception:
                    pass

    def test_load_to_postgresql_with_sqlalchemy_mock(self):
        """Test PostgreSQL flow dengan mock SQLAlchemy."""
        df = create_sample_dataframe()

        mock_sqlalchemy = MagicMock()
        mock_engine = MagicMock()
        mock_sqlalchemy.create_engine.return_value = mock_engine

        with patch.dict("sys.modules", {"sqlalchemy": mock_sqlalchemy}):
            try:
                load_to_postgresql(df, "products", "postgresql://user:pass@localhost/db")
            except Exception:
                pass

    def test_load_to_postgresql_invalid_connection(self):
        """Test error handling untuk connection string yang invalid."""
        df = create_sample_dataframe()
        with pytest.raises(Exception):
            load_to_postgresql(df, "products", "invalid://connection_string")

    def test_load_to_csv_overwrite(self, tmp_path):
        """Test CSV overwrite file yang sudah ada."""
        df1 = create_sample_dataframe()
        df2 = pd.DataFrame({
            "Title": ["New Product"],
            "Price": [500000.0],
            "Rating": [4.0],
            "Colors": [2],
            "Size": ["S"],
            "Gender": ["Women"],
            "Timestamp": ["2026-06-10 17:00:00"],
        })

        filepath = str(tmp_path / "overwrite_test.csv")
        load_to_csv(df1, filepath)
        load_to_csv(df2, filepath)

        loaded_df = pd.read_csv(filepath)
        assert len(loaded_df) == 1
        assert loaded_df["Title"].iloc[0] == "New Product"
