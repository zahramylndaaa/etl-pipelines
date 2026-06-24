import pandas as pd

from utils.transform import transform_to_dataframe, transform_data


def test_transform_to_dataframe():
    """Test mengubah data list menjadi DataFrame."""

    data = [
        {
            "Title": "T-shirt 1",
            "Price": "$100.00",
            "Rating": "Rating: ⭐ 4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "Timestamp": "2025-01-01T10:00:00"
        }
    ]

    result = transform_to_dataframe(data)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1


def test_transform_data_cleaning():
    """Test transformasi dan pembersihan data."""

    data = pd.DataFrame([
        {
            "Title": "T-shirt 1",
            "Price": "$100.00",
            "Rating": "Rating: ⭐ 4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "Timestamp": "2025-01-01T10:00:00"
        },
        {
            "Title": "Unknown Product",
            "Price": "$100.00",
            "Rating": "Rating: ⭐ Invalid Rating / 5",
            "Colors": "5 Colors",
            "Size": "Size: L",
            "Gender": "Gender: Women",
            "Timestamp": "2025-01-01T10:00:00"
        }
    ])

    result = transform_data(data)

    assert len(result) == 1
    assert result.iloc[0]["Title"] == "T-shirt 1"
    assert result.iloc[0]["Price"] == 1600000.0
    assert result.iloc[0]["Rating"] == 4.5
    assert result.iloc[0]["Colors"] == 3
    assert result.iloc[0]["Size"] == "M"
    assert result.iloc[0]["Gender"] == "Men"