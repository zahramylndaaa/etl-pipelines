import os
from unittest.mock import patch, Mock, MagicMock

import pandas as pd

from utils.load import store_to_csv, store_to_postgre, store_to_google_sheets


def test_store_to_csv():
    """Test penyimpanan data ke CSV."""

    data = pd.DataFrame([
        {
            "Title": "T-shirt 1",
            "Price": 1600000.0,
            "Rating": 4.5,
            "Colors": 3,
            "Size": "M",
            "Gender": "Men",
            "Timestamp": "2025-01-01"
        }
    ])

    filename = "test_products.csv"

    store_to_csv(data, filename)

    assert os.path.exists(filename)

    loaded_data = pd.read_csv(filename)

    assert len(loaded_data) == 1
    assert loaded_data.iloc[0]["Title"] == "T-shirt 1"

    os.remove(filename)


@patch("utils.load.create_engine")
def test_store_to_postgre(mock_create_engine):
    """Test penyimpanan data ke PostgreSQL."""

    data = pd.DataFrame([
        {
            "Title": "T-shirt 1",
            "Price": 1600000.0
        }
    ])

    mock_engine = MagicMock()
    mock_connection = MagicMock()

    mock_engine.connect.return_value.__enter__.return_value = mock_connection
    mock_create_engine.return_value = mock_engine

    store_to_postgre(
        data,
        "postgresql+psycopg2://postgres:password@localhost:5432/fashiondb"
    )

    assert mock_create_engine.called
    assert mock_engine.connect.called


@patch("utils.load.build")
@patch("utils.load.Credentials.from_service_account_file")
def test_store_to_google_sheets(mock_credentials, mock_build):
    """Test penyimpanan data ke Google Sheets."""

    data = pd.DataFrame([
        {
            "Title": "T-shirt 1",
            "Price": 1600000.0
        }
    ])

    mock_credentials.return_value = Mock()

    mock_service = Mock()
    mock_sheet = Mock()

    mock_service.spreadsheets.return_value = mock_sheet
    mock_sheet.values.return_value.update.return_value.execute.return_value = {}

    mock_build.return_value = mock_service

    store_to_google_sheets(
        data,
        "spreadsheet_id",
        "Sheet1!A1",
        "google-sheets-api.json"
    )

    assert mock_credentials.called
    assert mock_build.called
    assert mock_sheet.values.return_value.update.called