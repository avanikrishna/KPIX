import mysql.connector
import pandas as pd


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="kpix"
    )


def load_sales_data():
    connection = get_connection()

    query = "SELECT * FROM sales"

    df = pd.read_sql(query, connection)

    connection.close()

    return df