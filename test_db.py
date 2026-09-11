import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

server = os.getenv("DB_SERVER")
database = os.getenv("DB_DATABASE")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server},1433;"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(connection_string)

    cursor = conn.cursor()
    cursor.execute("SELECT DB_NAME()")

    result = cursor.fetchone()

    print("Database connection successful!")
    print("Connected database:", result[0])

    cursor.close()
    conn.close()

except Exception as e:
    print("Database connection failed!")
    print(e)
