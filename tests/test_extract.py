from unittest.mock import patch, Mock

from utils.extract import fetching_content
from utils.extract import extract_product_data


@patch("utils.extract.requests.Session")
def test_fetching_content_success(mock_session):
    """Test fetching_content ketika request berhasil."""

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"<html><body>Test</body></html>"

    mock_session.return_value.get.return_value = mock_response

    result = fetching_content("https://example.com")

    assert result == b"<html><body>Test</body></html>"


def test_extract_product_data():
    """Test extract_product_data."""

    from bs4 import BeautifulSoup

    html = """
    <div class="collection-card">
        <div class="product-details">
            <h3 class="product-title">T-shirt 1</h3>

            <span class="price">$100.00</span>

            <p>Rating: ⭐ 4.5 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Men</p>
        </div>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")

    card = soup.find("div", class_="collection-card")

    result = extract_product_data(card)

    assert result["Title"] == "T-shirt 1"
    assert result["Price"] == "$100.00"
    assert result["Rating"] == "Rating: ⭐ 4.5 / 5"

@patch("utils.extract.fetching_content")
def test_scrape_main(mock_fetching_content):
    """Test scrape_main."""

    html = """
    <html>
        <body>
            <div class="collection-card">
                <div class="product-details">
                    <h3 class="product-title">T-shirt Test</h3>

                    <span class="price">$100.00</span>

                    <p>Rating: ⭐ 4.5 / 5</p>
                    <p>3 Colors</p>
                    <p>Size: M</p>
                    <p>Gender: Men</p>
                </div>
            </div>
        </body>
    </html>
    """

    mock_fetching_content.return_value = html

    from utils.extract import scrape_main

    result = scrape_main("https://example.com/", 1, 1)

    assert len(result) == 1
    assert result[0]["Title"] == "T-shirt Test"