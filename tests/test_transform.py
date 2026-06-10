"""
Unit tests untuk modul Transform.
Menguji fungsi pembersihan data: clean_price, clean_rating, clean_colors,
clean_size, clean_gender, remove_invalid_data, remove_duplicates, dan transform_data.
"""

import pytest
import pandas as pd
import numpy as np
from utils.transform import (
    clean_price,
    clean_rating,
    clean_colors,
    clean_size,
    clean_gender,
    remove_invalid_data,
    remove_duplicates,
    transform_data,
)


# ======================================================
# Tests untuk clean_price
# ======================================================
class TestCleanPrice:
    """Test class untuk fungsi clean_price."""

    def test_clean_price_normal(self):
        """Test konversi harga normal: $269.98 -> 4_319_680.0"""
        series = pd.Series(["$269.98"])
        result = clean_price(series)
        assert result.iloc[0] == 269.98 * 16000

    def test_clean_price_whole_number(self):
        """Test konversi harga bulat: $50.00 -> 800_000.0"""
        series = pd.Series(["$50.00"])
        result = clean_price(series)
        assert result.iloc[0] == 50.00 * 16000

    def test_clean_price_with_comma(self):
        """Test konversi harga dengan koma: $1,250.00 -> 20_000_000.0"""
        series = pd.Series(["$1,250.00"])
        result = clean_price(series)
        assert result.iloc[0] == 1250.00 * 16000

    def test_clean_price_multiple(self):
        """Test konversi beberapa harga sekaligus."""
        series = pd.Series(["$100.00", "$200.50", "$300.75"])
        result = clean_price(series)
        assert len(result) == 3
        assert result.iloc[0] == 100.00 * 16000
        assert result.iloc[1] == 200.50 * 16000
        assert result.iloc[2] == 300.75 * 16000

    def test_clean_price_invalid(self):
        """Test harga invalid menghasilkan NaN."""
        series = pd.Series(["invalid_price"])
        result = clean_price(series)
        assert pd.isna(result.iloc[0])


# ======================================================
# Tests untuk clean_rating
# ======================================================
class TestCleanRating:
    """Test class untuk fungsi clean_rating."""

    def test_clean_rating_valid(self):
        """Test rating valid: 'Rating: ⭐ 4.9 / 5' -> 4.9"""
        series = pd.Series(["Rating: ⭐ 4.9 / 5"])
        result = clean_rating(series)
        assert result.iloc[0] == 4.9

    def test_clean_rating_integer(self):
        """Test rating integer: 'Rating: ⭐ 4 / 5' -> 4.0"""
        series = pd.Series(["Rating: ⭐ 4 / 5"])
        result = clean_rating(series)
        assert result.iloc[0] == 4.0

    def test_clean_rating_invalid(self):
        """Test rating invalid: 'Rating: ⭐ Invalid Rating / 5' -> NaN"""
        series = pd.Series(["Rating: ⭐ Invalid Rating / 5"])
        result = clean_rating(series)
        assert pd.isna(result.iloc[0])

    def test_clean_rating_multiple(self):
        """Test beberapa rating valid."""
        series = pd.Series([
            "Rating: ⭐ 4.5 / 5",
            "Rating: ⭐ 3.8 / 5",
            "Rating: ⭐ 5.0 / 5",
        ])
        result = clean_rating(series)
        assert result.iloc[0] == 4.5
        assert result.iloc[1] == 3.8
        assert result.iloc[2] == 5.0

    def test_clean_rating_mixed_valid_invalid(self):
        """Test campuran rating valid dan invalid."""
        series = pd.Series([
            "Rating: ⭐ 4.5 / 5",
            "Rating: ⭐ Invalid Rating / 5",
            "Rating: ⭐ 3.0 / 5",
        ])
        result = clean_rating(series)
        assert result.iloc[0] == 4.5
        assert pd.isna(result.iloc[1])
        assert result.iloc[2] == 3.0


# ======================================================
# Tests untuk clean_colors
# ======================================================
class TestCleanColors:
    """Test class untuk fungsi clean_colors."""

    def test_clean_colors_normal(self):
        """Test: '3 Colors' -> 3"""
        series = pd.Series(["3 Colors"])
        result = clean_colors(series)
        assert result.iloc[0] == 3

    def test_clean_colors_five(self):
        """Test: '5 Colors' -> 5"""
        series = pd.Series(["5 Colors"])
        result = clean_colors(series)
        assert result.iloc[0] == 5

    def test_clean_colors_multiple(self):
        """Test beberapa data warna."""
        series = pd.Series(["3 Colors", "5 Colors", "2 Colors"])
        result = clean_colors(series)
        assert result.iloc[0] == 3
        assert result.iloc[1] == 5
        assert result.iloc[2] == 2

    def test_clean_colors_invalid(self):
        """Test warna invalid menghasilkan NaN."""
        series = pd.Series(["No color info"])
        result = clean_colors(series)
        assert pd.isna(result.iloc[0])


# ======================================================
# Tests untuk clean_size
# ======================================================
class TestCleanSize:
    """Test class untuk fungsi clean_size."""

    def test_clean_size_m(self):
        """Test: 'Size: M' -> 'M'"""
        series = pd.Series(["Size: M"])
        result = clean_size(series)
        assert result.iloc[0] == "M"

    def test_clean_size_xl(self):
        """Test: 'Size: XL' -> 'XL'"""
        series = pd.Series(["Size: XL"])
        result = clean_size(series)
        assert result.iloc[0] == "XL"

    def test_clean_size_multiple(self):
        """Test beberapa data ukuran."""
        series = pd.Series(["Size: S", "Size: M", "Size: L", "Size: XL", "Size: XXL"])
        result = clean_size(series)
        expected = ["S", "M", "L", "XL", "XXL"]
        assert list(result) == expected


# ======================================================
# Tests untuk clean_gender
# ======================================================
class TestCleanGender:
    """Test class untuk fungsi clean_gender."""

    def test_clean_gender_men(self):
        """Test: 'Gender: Men' -> 'Men'"""
        series = pd.Series(["Gender: Men"])
        result = clean_gender(series)
        assert result.iloc[0] == "Men"

    def test_clean_gender_women(self):
        """Test: 'Gender: Women' -> 'Women'"""
        series = pd.Series(["Gender: Women"])
        result = clean_gender(series)
        assert result.iloc[0] == "Women"

    def test_clean_gender_unisex(self):
        """Test: 'Gender: Unisex' -> 'Unisex'"""
        series = pd.Series(["Gender: Unisex"])
        result = clean_gender(series)
        assert result.iloc[0] == "Unisex"

    def test_clean_gender_multiple(self):
        """Test beberapa data gender."""
        series = pd.Series(["Gender: Men", "Gender: Women", "Gender: Unisex"])
        result = clean_gender(series)
        expected = ["Men", "Women", "Unisex"]
        assert list(result) == expected


# ======================================================
# Tests untuk remove_invalid_data
# ======================================================
class TestRemoveInvalidData:
    """Test class untuk fungsi remove_invalid_data."""

    def test_remove_unknown_product(self):
        """Test penghapusan baris 'Unknown Product'."""
        df = pd.DataFrame({
            "Title": ["T-shirt 1", "Unknown Product", "Hoodie 3"],
            "Price": ["$50.00", "$100.00", "$120.00"],
        })
        result = remove_invalid_data(df)
        assert len(result) == 2
        assert "Unknown Product" not in result["Title"].values

    def test_remove_multiple_unknown(self):
        """Test penghapusan beberapa baris 'Unknown Product'."""
        df = pd.DataFrame({
            "Title": ["Unknown Product", "Pants 2", "Unknown Product", "Jacket 4"],
            "Price": ["$100.00", "$200.00", "$100.00", "$300.00"],
        })
        result = remove_invalid_data(df)
        assert len(result) == 2

    def test_no_invalid_data(self):
        """Test ketika tidak ada data invalid."""
        df = pd.DataFrame({
            "Title": ["T-shirt 1", "Hoodie 2", "Jacket 3"],
            "Price": ["$50.00", "$120.00", "$300.00"],
        })
        result = remove_invalid_data(df)
        assert len(result) == 3


# ======================================================
# Tests untuk remove_duplicates
# ======================================================
class TestRemoveDuplicates:
    """Test class untuk fungsi remove_duplicates."""

    def test_remove_duplicates(self):
        """Test penghapusan baris duplikat."""
        df = pd.DataFrame({
            "Title": ["T-shirt 1", "T-shirt 1", "Hoodie 2"],
            "Price": [800000.0, 800000.0, 1920000.0],
        })
        result = remove_duplicates(df)
        assert len(result) == 2

    def test_no_duplicates(self):
        """Test ketika tidak ada duplikat."""
        df = pd.DataFrame({
            "Title": ["T-shirt 1", "Hoodie 2", "Jacket 3"],
            "Price": [800000.0, 1920000.0, 4800000.0],
        })
        result = remove_duplicates(df)
        assert len(result) == 3


# ======================================================
# Tests untuk transform_data (integration)
# ======================================================
class TestTransformData:
    """Test class untuk fungsi transform_data (integrasi seluruh transformasi)."""

    def _create_raw_dataframe(self):
        """Helper: buat DataFrame data mentah simulasi."""
        return pd.DataFrame({
            "Title": ["T-shirt 1", "Unknown Product", "Hoodie 3", "T-shirt 1"],
            "Price": ["$50.00", "$100.00", "$120.50", "$50.00"],
            "Rating": [
                "Rating: ⭐ 4.5 / 5",
                "Rating: ⭐ Invalid Rating / 5",
                "Rating: ⭐ 3.8 / 5",
                "Rating: ⭐ 4.5 / 5",
            ],
            "Colors": ["3 Colors", "5 Colors", "5 Colors", "3 Colors"],
            "Size": ["Size: M", "Size: M", "Size: L", "Size: M"],
            "Gender": ["Gender: Men", "Gender: Men", "Gender: Women", "Gender: Men"],
            "Timestamp": ["2026-06-10 16:00:00"] * 4,
        })

    def test_transform_data_removes_invalid(self):
        """Test 'Unknown Product' dihapus setelah transformasi."""
        df = self._create_raw_dataframe()
        result = transform_data(df)
        assert "Unknown Product" not in result["Title"].values

    def test_transform_data_removes_duplicates(self):
        """Test duplikat dihapus setelah transformasi."""
        df = self._create_raw_dataframe()
        result = transform_data(df)
        assert len(result) == len(result.drop_duplicates())

    def test_transform_data_price_in_idr(self):
        """Test harga dikonversi ke IDR (× 16000)."""
        df = self._create_raw_dataframe()
        result = transform_data(df)
        # T-shirt 1: $50.00 * 16000 = 800000.0
        t_shirt = result[result["Title"] == "T-shirt 1"]
        assert t_shirt["Price"].iloc[0] == 800000.0

    def test_transform_data_rating_is_float(self):
        """Test rating bertipe float."""
        df = self._create_raw_dataframe()
        result = transform_data(df)
        assert result["Rating"].dtype == float

    def test_transform_data_colors_is_int(self):
        """Test colors bertipe integer."""
        df = self._create_raw_dataframe()
        result = transform_data(df)
        assert result["Colors"].dtype in [int, np.int64, np.int32]

    def test_transform_data_size_no_prefix(self):
        """Test kolom Size tidak memiliki prefix 'Size: '."""
        df = self._create_raw_dataframe()
        result = transform_data(df)
        for size in result["Size"]:
            assert not size.startswith("Size: ")

    def test_transform_data_gender_no_prefix(self):
        """Test kolom Gender tidak memiliki prefix 'Gender: '."""
        df = self._create_raw_dataframe()
        result = transform_data(df)
        for gender in result["Gender"]:
            assert not gender.startswith("Gender: ")

    def test_transform_data_no_null(self):
        """Test tidak ada nilai null setelah transformasi."""
        df = self._create_raw_dataframe()
        result = transform_data(df)
        assert result.isnull().sum().sum() == 0

    def test_transform_data_has_timestamp(self):
        """Test kolom Timestamp tetap ada setelah transformasi."""
        df = self._create_raw_dataframe()
        result = transform_data(df)
        assert "Timestamp" in result.columns

    def test_transform_data_index_reset(self):
        """Test index di-reset setelah transformasi."""
        df = self._create_raw_dataframe()
        result = transform_data(df)
        assert list(result.index) == list(range(len(result)))
