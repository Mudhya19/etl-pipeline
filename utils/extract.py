"""
Extract module - Web scraping dari fashion-studio.dicoding.dev
Mengambil data produk dari 50 halaman website.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


BASE_URL = "https://fashion-studio.dicoding.dev/"


def fetch_page(url):
    """
    Mengambil konten HTML dari sebuah URL.
    
    Args:
        url (str): URL halaman yang akan di-fetch.
    
    Returns:
        str: Konten HTML halaman, atau None jika gagal.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_products(html):
    """
    Mem-parsing data produk dari konten HTML.
    
    Args:
        html (str): String HTML yang berisi data produk.
    
    Returns:
        list[dict]: List dictionary berisi data produk mentah.
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
        products = []
        cards = soup.find_all("div", class_="collection-card")

        for card in cards:
            try:
                product_details = card.find("div", class_="product-details")
                p_tags = product_details.find_all("p")

                product = {
                    "Title": card.find("h3", class_="product-title").text.strip(),
                    "Price": card.find("span", class_="price").text.strip(),
                    "Rating": p_tags[0].text.strip(),
                    "Colors": p_tags[1].text.strip(),
                    "Size": p_tags[2].text.strip(),
                    "Gender": p_tags[3].text.strip(),
                }
                products.append(product)
            except (AttributeError, IndexError) as e:
                print(f"Error parsing product card: {e}")
                continue

        return products
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return []


def scrape_page(page_number):
    """
    Melakukan scraping produk dari satu halaman.
    
    Args:
        page_number (int): Nomor halaman (1-50).
    
    Returns:
        list[dict]: List dictionary berisi data produk dari halaman tersebut.
    """
    try:
        if page_number == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}page{page_number}.html"

        html = fetch_page(url)
        if html is None:
            return []

        return parse_products(html)
    except Exception as e:
        print(f"Error scraping page {page_number}: {e}")
        return []


def scrape_all_pages(start=1, end=50):
    """
    Melakukan scraping seluruh halaman dan mengembalikan DataFrame dengan timestamp.
    
    Args:
        start (int): Halaman awal (default: 1).
        end (int): Halaman akhir (default: 50).
    
    Returns:
        pd.DataFrame: DataFrame berisi semua data produk mentah dengan kolom Timestamp.
    """
    try:
        all_products = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for page in range(start, end + 1):
            print(f"Scraping page {page}/{end}...")
            products = scrape_page(page)
            all_products.extend(products)

        df = pd.DataFrame(all_products)
        if not df.empty:
            df["Timestamp"] = timestamp

        print(f"Total products scraped: {len(df)}")
        return df
    except Exception as e:
        print(f"Error in scrape_all_pages: {e}")
        return pd.DataFrame()
