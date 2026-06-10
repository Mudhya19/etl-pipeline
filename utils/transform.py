"""
Transform module - Pembersihan dan transformasi data produk.
Mengonversi format data mentah menjadi format bersih sesuai spesifikasi.
"""

import pandas as pd


def clean_price(price_series):
    """
    Mengonversi harga dari string USD ke float IDR.
    Contoh: "$269.98" -> 4_319_680.0 (× 16000)
    
    Args:
        price_series (pd.Series): Kolom harga dalam format string USD.
    
    Returns:
        pd.Series: Kolom harga dalam float IDR.
    """
    try:
        cleaned = price_series.str.replace("$", "", regex=False).str.replace(",", "", regex=False)
        return pd.to_numeric(cleaned, errors="coerce") * 16000
    except Exception as e:
        print(f"Error cleaning price: {e}")
        raise


def clean_rating(rating_series):
    """
    Mengekstrak nilai rating numerik dari string.
    Contoh: "Rating: ⭐ 4.9 / 5" -> 4.9
    "Rating: ⭐ Invalid Rating / 5" -> NaN
    
    Args:
        rating_series (pd.Series): Kolom rating dalam format string.
    
    Returns:
        pd.Series: Kolom rating dalam float.
    """
    try:
        extracted = rating_series.str.extract(r"(\d+\.?\d*)\s*/\s*5")
        return pd.to_numeric(extracted[0], errors="coerce")
    except Exception as e:
        print(f"Error cleaning rating: {e}")
        raise


def clean_colors(colors_series):
    """
    Mengekstrak angka jumlah warna dari string.
    Contoh: "3 Colors" -> 3
    
    Args:
        colors_series (pd.Series): Kolom warna dalam format string.
    
    Returns:
        pd.Series: Kolom warna dalam numeric (float, akan dikonversi ke int setelah dropna).
    """
    try:
        extracted = colors_series.str.extract(r"(\d+)")
        return pd.to_numeric(extracted[0], errors="coerce")
    except Exception as e:
        print(f"Error cleaning colors: {e}")
        raise


def clean_size(size_series):
    """
    Menghapus prefix "Size: " dari string ukuran.
    Contoh: "Size: M" -> "M"
    
    Args:
        size_series (pd.Series): Kolom ukuran dalam format string.
    
    Returns:
        pd.Series: Kolom ukuran tanpa prefix.
    """
    try:
        return size_series.str.replace("Size: ", "", regex=False)
    except Exception as e:
        print(f"Error cleaning size: {e}")
        raise


def clean_gender(gender_series):
    """
    Menghapus prefix "Gender: " dari string gender.
    Contoh: "Gender: Men" -> "Men"
    
    Args:
        gender_series (pd.Series): Kolom gender dalam format string.
    
    Returns:
        pd.Series: Kolom gender tanpa prefix.
    """
    try:
        return gender_series.str.replace("Gender: ", "", regex=False)
    except Exception as e:
        print(f"Error cleaning gender: {e}")
        raise


def remove_invalid_data(df):
    """
    Menghapus baris dengan data invalid seperti 'Unknown Product'.
    
    Args:
        df (pd.DataFrame): DataFrame dengan data mentah.
    
    Returns:
        pd.DataFrame: DataFrame tanpa baris invalid.
    """
    try:
        df = df[df["Title"] != "Unknown Product"].copy()
        return df
    except Exception as e:
        print(f"Error removing invalid data: {e}")
        raise


def remove_duplicates(df):
    """
    Menghapus baris duplikat dari DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame input.
    
    Returns:
        pd.DataFrame: DataFrame tanpa duplikat.
    """
    try:
        return df.drop_duplicates()
    except Exception as e:
        print(f"Error removing duplicates: {e}")
        raise


def transform_data(df):
    """
    Menjalankan seluruh proses transformasi data.
    
    Urutan:
    1. Hapus produk invalid (Unknown Product)
    2. Bersihkan kolom Price (USD -> IDR × 16000)
    3. Bersihkan kolom Rating (ekstrak float)
    4. Bersihkan kolom Colors (ekstrak angka)
    5. Bersihkan kolom Size (hapus prefix "Size: ")
    6. Bersihkan kolom Gender (hapus prefix "Gender: ")
    7. Hapus baris dengan nilai null
    8. Konversi Colors ke integer
    9. Hapus duplikat
    10. Reset index
    
    Args:
        df (pd.DataFrame): DataFrame data mentah.
    
    Returns:
        pd.DataFrame: DataFrame data bersih.
    """
    try:
        # 1. Hapus produk invalid
        df = remove_invalid_data(df)

        # 2. Bersihkan setiap kolom
        df["Price"] = clean_price(df["Price"])
        df["Rating"] = clean_rating(df["Rating"])
        df["Colors"] = clean_colors(df["Colors"])
        df["Size"] = clean_size(df["Size"])
        df["Gender"] = clean_gender(df["Gender"])

        # 3. Hapus baris dengan nilai null (dari konversi yang gagal)
        df = df.dropna()

        # 4. Konversi Colors ke integer setelah dropna
        df["Colors"] = df["Colors"].astype(int)

        # 5. Hapus duplikat
        df = remove_duplicates(df)

        # 6. Reset index
        df = df.reset_index(drop=True)

        print(f"Data after transformation: {len(df)} rows")
        return df
    except Exception as e:
        print(f"Error in transform_data: {e}")
        raise
