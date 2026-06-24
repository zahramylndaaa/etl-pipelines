from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def store_to_csv(data, filename="products.csv"):
    """Menyimpan data ke dalam berkas CSV."""

    try:
        data.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}")

    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke CSV: {e}")


def store_to_postgre(data, db_url, table_name="products"):
    """Menyimpan data ke dalam PostgreSQL."""

    try:
        engine = create_engine(db_url)

        with engine.connect() as connection:
            data.to_sql(
                table_name,
                con=connection,
                if_exists="replace",
                index=False
            )

        print("Data berhasil disimpan ke PostgreSQL!")

    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke PostgreSQL: {e}")


def store_to_google_sheets(data, spreadsheet_id, range_name, credential_file):
    """Menyimpan data ke dalam Google Sheets."""

    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]

        credentials = Credentials.from_service_account_file(
            credential_file,
            scopes=scopes
        )

        service = build("sheets", "v4", credentials=credentials)

        values = [data.columns.values.tolist()] + data.astype(str).values.tolist()

        body = {
            "values": values
        }

        sheet = service.spreadsheets()

        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()

        print("Data berhasil disimpan ke Google Sheets!")

    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke Google Sheets: {e}")