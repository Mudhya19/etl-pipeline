"""
Unit tests untuk modul Extract.
Menguji fungsi fetch_page, parse_products, scrape_page, dan scrape_all_pages.
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.extract import fetch_page, parse_products, scrape_page, scrape_all_pages


# ======================================================
# Sample HTML untuk testing
# ======================================================
SAMPLE_HTML = """
<html>
<body>
<div class="collection-grid" id="collectionList">
    <div class="collection-card">
        <div style="position: relative;">
            <img src="test.jpg" class="collection-image" alt="T-shirt 1">
        </div>
        <div class="product-details">
            <h3 class="product-title">T-shirt 1</h3>
            <div class="price-container"><span class="price">$50.00</span></div>
            <p style="font-size: 14px; color: #777;">Rating: ⭐ 4.5 / 5</p>
            <p style="font-size: 14px; color: #777;">3 Colors</p>
            <p style="font-size: 14px; color: #777;">Size: M</p>
            <p style="font-size: 14px; color: #777;">Gender: Men</p>
        </div>
    </div>
    <div class="collection-card">
        <div style="position: relative;">
            <img src="test2.jpg" class="collection-image" alt="Hoodie 2">
        </div>
        <div class="product-details">
            <h3 class="product-title">Hoodie 2</h3>
            <div class="price-container"><span class="price">$120.50</span></div>
            <p style="font-size: 14px; color: #777;">Rating: ⭐ 3.8 / 5</p>
            <p style="font-size: 14px; color: #777;">5 Colors</p>
            <p style="font-size: 14px; color: #777;">Size: L</p>
            <p style="font-size: 14px; color: #777;">Gender: Women</p>
        </div>
    </div>
    <div class="collection-card">
        <div style="position: relative;">
            <img src="test3.jpg" class="collection-image" alt="Unknown Product">
        </div>
        <div class="product-details">
            <h3 class="product-title">Unknown Product</h3>
            <div class="price-container"><span class="price">$100.00</span></div>
            <p style="font-size: 14px; color: #777;">Rating: ⭐ Invalid Rating / 5</p>
            <p style="font-size: 14px; color: #777;">5 Colors</p>
            <p style="font-size: 14px; color: #777;">Size: M</p>
            <p style="font-size: 14px; color: #777;">Gender: Men</p>
        </div>
    </div>
</div>
</body>
</html>
"""

EMPTY_HTML = "<html><body></body></html>"

MALFORMED_HTML = """
<html>
<body>
<div class="collection-card">
    <div class="product-details">
        <h3 class="product-title">Broken Product</h3>
    </div>
</div>
</body>
</html>
"""


# ======================================================
# Tests untuk fetch_page
# ======================================================
class TestFetchPage:
    """Test class untuk fungsi fetch_page."""

    @patch("utils.extract.requests.get")
    def test_fetch_page_success(self, mock_get):
        """Test fetch halaman berhasil."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = SAMPLE_HTML
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_page("https://fashion-studio.dicoding.dev/")
        assert result == SAMPLE_HTML
        mock_get.assert_called_once_with("https://fashion-studio.dicoding.dev/", timeout=10)

    @patch("utils.extract.requests.get")
    def test_fetch_page_http_error(self, mock_get):
        """Test fetch halaman dengan HTTP error (404, 500, dll)."""
        import requests
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        result = fetch_page("https://fashion-studio.dicoding.dev/page999.html")
        assert result is None

    @patch("utils.extract.requests.get")
    def test_fetch_page_connection_error(self, mock_get):
        """Test fetch halaman dengan connection error."""
        import requests
        mock_get.side_effect = requests.ConnectionError("Connection refused")

        result = fetch_page("https://fashion-studio.dicoding.dev/")
        assert result is None

    @patch("utils.extract.requests.get")
    def test_fetch_page_timeout(self, mock_get):
        """Test fetch halaman dengan timeout."""
        import requests
        mock_get.side_effect = requests.Timeout("Request timed out")

        result = fetch_page("https://fashion-studio.dicoding.dev/")
        assert result is None


# ======================================================
# Tests untuk parse_products
# ======================================================
class TestParseProducts:
    """Test class untuk fungsi parse_products."""

    def test_parse_products_valid_html(self):
        """Test parsing HTML valid dengan 3 produk."""
        products = parse_products(SAMPLE_HTML)
        assert len(products) == 3
        assert products[0]["Title"] == "T-shirt 1"
        assert products[0]["Price"] == "$50.00"
        assert products[0]["Rating"] == "Rating: ⭐ 4.5 / 5"
        assert products[0]["Colors"] == "3 Colors"
        assert products[0]["Size"] == "Size: M"
        assert products[0]["Gender"] == "Gender: Men"

    def test_parse_products_second_product(self):
        """Test data produk kedua parsed dengan benar."""
        products = parse_products(SAMPLE_HTML)
        assert products[1]["Title"] == "Hoodie 2"
        assert products[1]["Price"] == "$120.50"
        assert products[1]["Rating"] == "Rating: ⭐ 3.8 / 5"
        assert products[1]["Colors"] == "5 Colors"
        assert products[1]["Size"] == "Size: L"
        assert products[1]["Gender"] == "Gender: Women"

    def test_parse_products_invalid_product(self):
        """Test data produk invalid (Unknown Product) tetap ter-parse di tahap extract."""
        products = parse_products(SAMPLE_HTML)
        assert products[2]["Title"] == "Unknown Product"
        assert products[2]["Rating"] == "Rating: ⭐ Invalid Rating / 5"

    def test_parse_products_empty_html(self):
        """Test parsing HTML tanpa produk."""
        products = parse_products(EMPTY_HTML)
        assert len(products) == 0

    def test_parse_products_malformed_html(self):
        """Test parsing HTML yang rusak (elemen tidak lengkap)."""
        products = parse_products(MALFORMED_HTML)
        # Produk yang rusak di-skip karena error handling
        assert len(products) == 0

    def test_parse_products_none_input(self):
        """Test parsing None sebagai input."""
        products = parse_products(None)
        assert products == []


# ======================================================
# Tests untuk scrape_page
# ======================================================
class TestScrapePage:
    """Test class untuk fungsi scrape_page."""

    @patch("utils.extract.fetch_page")
    def test_scrape_page_success(self, mock_fetch):
        """Test scraping satu halaman berhasil."""
        mock_fetch.return_value = SAMPLE_HTML
        products = scrape_page(2)
        assert len(products) == 3
        mock_fetch.assert_called_once_with("https://fashion-studio.dicoding.dev/page2.html")

    @patch("utils.extract.fetch_page")
    def test_scrape_page_first_page(self, mock_fetch):
        """Test URL halaman pertama menggunakan base URL."""
        mock_fetch.return_value = SAMPLE_HTML
        products = scrape_page(1)
        assert len(products) == 3
        mock_fetch.assert_called_once_with("https://fashion-studio.dicoding.dev/")

    @patch("utils.extract.fetch_page")
    def test_scrape_page_fetch_fails(self, mock_fetch):
        """Test scraping ketika fetch gagal (return None)."""
        mock_fetch.return_value = None
        products = scrape_page(5)
        assert len(products) == 0

    @patch("utils.extract.fetch_page")
    def test_scrape_page_url_pattern(self, mock_fetch):
        """Test URL pattern untuk halaman selain halaman 1."""
        mock_fetch.return_value = EMPTY_HTML
        scrape_page(50)
        mock_fetch.assert_called_once_with("https://fashion-studio.dicoding.dev/page50.html")


# ======================================================
# Tests untuk scrape_all_pages
# ======================================================
class TestScrapeAllPages:
    """Test class untuk fungsi scrape_all_pages."""

    @patch("utils.extract.scrape_page")
    def test_scrape_all_pages_success(self, mock_scrape):
        """Test scraping seluruh halaman berhasil dan menghasilkan DataFrame dengan Timestamp."""
        mock_scrape.return_value = [
            {
                "Title": "T-shirt 1",
                "Price": "$50.00",
                "Rating": "Rating: ⭐ 4.5 / 5",
                "Colors": "3 Colors",
                "Size": "Size: M",
                "Gender": "Gender: Men",
            }
        ]

        df = scrape_all_pages(start=1, end=3)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3  # 1 produk × 3 halaman
        assert "Timestamp" in df.columns
        assert mock_scrape.call_count == 3

    @patch("utils.extract.scrape_page")
    def test_scrape_all_pages_empty(self, mock_scrape):
        """Test scraping ketika semua halaman kosong."""
        mock_scrape.return_value = []
        df = scrape_all_pages(start=1, end=2)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    @patch("utils.extract.scrape_page")
    def test_scrape_all_pages_has_all_columns(self, mock_scrape):
        """Test DataFrame memiliki semua kolom yang dibutuhkan."""
        mock_scrape.return_value = [
            {
                "Title": "Pants 10",
                "Price": "$200.00",
                "Rating": "Rating: ⭐ 4.0 / 5",
                "Colors": "5 Colors",
                "Size": "Size: XL",
                "Gender": "Gender: Unisex",
            }
        ]
        df = scrape_all_pages(start=1, end=1)
        expected_columns = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "Timestamp"]
        for col in expected_columns:
            assert col in df.columns

    @patch("utils.extract.scrape_page")
    def test_scrape_all_pages_single_page(self, mock_scrape):
        """Test scraping hanya satu halaman."""
        mock_scrape.return_value = [
            {
                "Title": "Jacket 5",
                "Price": "$300.00",
                "Rating": "Rating: ⭐ 3.5 / 5",
                "Colors": "2 Colors",
                "Size": "Size: S",
                "Gender": "Gender: Women",
            }
        ]
        df = scrape_all_pages(start=5, end=5)
        assert len(df) == 1
        assert mock_scrape.call_count == 1
