import json
import os
import pyodbc
from datetime import datetime


SERVER = "xxxxx"
DATABASE = "ProductDataPlatform_V3"
BRONZE_FOLDER = "."


def find_latest_json():
    files = [
        file
        for file in os.listdir(BRONZE_FOLDER)
        if file.startswith("products_") and file.endswith(".json")
    ]

    if not files:
        raise FileNotFoundError("No Bronze JSON files found.")

    return max(files)


def read_json(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


def connect_to_sql_server():
    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string)


def load_bronze(connection, file_name, data):

    raw_json = json.dumps(
        data,
        ensure_ascii=False
    )

    sql = """
        INSERT INTO bronze.products_raw
        (
            source,
            file_name,
            raw_data
        )
        VALUES (?, ?, ?)
    """

    cursor = connection.cursor()

    cursor.execute(
        sql,
        "DummyJSON API",
        file_name,
        raw_json
    )

    connection.commit()

    cursor.close()


def main():

    print("Starting Bronze load...")

    file_name = find_latest_json()

    print(f"Reading file: {file_name}")

    data = read_json(file_name)

    print("Connecting to SQL Server...")

    connection = connect_to_sql_server()

    load_bronze(
        connection,
        file_name,
        data
    )

    connection.close()

    print("Bronze load completed successfully.")


if __name__ == "__main__":
    main()
