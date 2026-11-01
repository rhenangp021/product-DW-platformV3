import pyodbc

SERVER = "xxxxx"
DATABASE = "ProductDataPlatform_V3"

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

try:
    connection = pyodbc.connect(connection_string)

    print("SQL Server connection successful!")

    connection.close()

except Exception as error:
    print("Connection failed:")
    print(error)
