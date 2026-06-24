from utils.extract import scrape_main
from utils.transform import transform_to_dataframe, transform_data
from utils.load import store_to_csv, store_to_postgre, store_to_google_sheets


def main():
    """Fungsi utama untuk menjalankan proses ETL pipeline."""

    BASE_URL = "https://fashion-studio.dicoding.dev/"

    DB_URL = "postgresql+psycopg2://postgres:zahra123@localhost:5432/fashiondb"

    SPREADSHEET_ID = "1aO7rcAtWFg6FRJfl2Px-9ZUm3zEIGkcXSZSbadIKk-8"
    RANGE_NAME = "Sheet1!A1"
    CREDENTIAL_FILE = "google-sheets-api.json"

    products = scrape_main(BASE_URL)

    if products:
        dataframe = transform_to_dataframe(products)
        clean_data = transform_data(dataframe)

        print(f"Jumlah data awal: {len(dataframe)}")
        print(f"Jumlah data setelah transformasi: {len(clean_data)}")

        store_to_csv(clean_data)
        store_to_postgre(clean_data, DB_URL)
        store_to_google_sheets(
            clean_data,
            SPREADSHEET_ID,
            RANGE_NAME,
            CREDENTIAL_FILE
        )

    else:
        print("Tidak ada data yang berhasil diambil.")


if __name__ == "__main__":
    main()