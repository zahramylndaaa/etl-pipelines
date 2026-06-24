import pandas as pd


def transform_to_dataframe(data):
    """Mengubah data hasil scraping menjadi DataFrame."""

    try:
        dataframe = pd.DataFrame(data)
        return dataframe

    except Exception as e:
        print(f"Error mengubah data menjadi DataFrame: {e}")
        return pd.DataFrame()


def transform_data(data, exchange_rate=16000):
    """Membersihkan dan mentransformasi data produk."""

    try:
        data = data.copy()

        data = data.replace({
            "Title": {
                "Unknown Product": None
            },
            "Price": {
                "Price Unavailable": None
            },
            "Rating": {
                "Rating: ⭐ Invalid Rating / 5": None,
                "Not Rated": None
            }
        })

        data = data.dropna()
        data = data.drop_duplicates()

        data["Price"] = (
            data["Price"]
            .str.replace("$", "", regex=False)
            .astype(float)
            * exchange_rate
        )

        data["Rating"] = (
            data["Rating"]
            .str.extract(r"(\d+\.\d+)")
            .astype(float)
        )

        data["Colors"] = (
            data["Colors"]
            .str.extract(r"(\d+)")
            .astype(int)
        )

        data["Size"] = (
            data["Size"]
            .str.replace("Size:", "", regex=False)
            .str.strip()
            .astype("string")
        )

        data["Gender"] = (
            data["Gender"]
            .str.replace("Gender:", "", regex=False)
            .str.strip()
            .astype("string")
        )

        data["Title"] = data["Title"].astype("string")
        data["Price"] = data["Price"].astype(float)
        data["Rating"] = data["Rating"].astype(float)
        data["Colors"] = data["Colors"].astype(int)
        data["Timestamp"] = pd.to_datetime(data["Timestamp"])

        data = data.dropna()
        data = data.drop_duplicates()

        return data

    except Exception as e:
        print(f"Error saat transformasi data: {e}")
        return pd.DataFrame()