import requests
from bs4 import BeautifulSoup
from datetime import datetime


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/96.0.4664.110 Safari/537.36"
    )
}


def fetching_content(url):
    """Mengambil konten HTML dari website."""

    try:
        session = requests.Session()
        response = session.get(url, headers=HEADERS)

        response.raise_for_status()

        return response.content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching website: {e}")
        return None


def extract_product_data(card):
    """Mengambil data produk dari setiap card product."""

    try:
        title = card.find("h3", class_="product-title").text.strip()

        price_element = card.find(class_="price")
        price = price_element.text.strip() if price_element else None

        product_details = card.find("div", class_="product-details")
        info_text = product_details.find_all("p")

        rating = info_text[0].text.strip()
        colors = info_text[1].text.strip()
        size = info_text[2].text.strip()
        gender = info_text[3].text.strip()

        timestamp = datetime.now().isoformat()

        product = {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp
        }

        return product

    except Exception as e:
        print(f"Error extracting product data: {e}")
        return None


def scrape_main(base_url, start_page=1, end_page=50):
    """Melakukan scraping data dari seluruh halaman website."""

    products = []

    try:
        for page in range(start_page, end_page + 1):

            if page == 1:
                url = base_url
            else:
                url = f"{base_url}page{page}"

            print(f"Scraping page {page}: {url}")

            content = fetching_content(url)

            if content:

                soup = BeautifulSoup(content, "html.parser")

                cards = soup.find_all("div", class_="collection-card")

                for card in cards:

                    product = extract_product_data(card)

                    if product:
                        products.append(product)

        return products

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None