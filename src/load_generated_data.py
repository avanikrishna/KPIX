import mysql.connector
import pandas as pd


def load_csv_to_mysql():

    df = pd.read_csv("data/sales.csv")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        database="kpix"
    )

    cursor = connection.cursor()

    # Remove old sales data
    cursor.execute("DELETE FROM sales")

    # Insert new data
    query = """
        INSERT INTO sales
        (sale_date, region, category, product,
         customer_id, quantity, unit_price, revenue)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():

        cursor.execute(
            query,
            (
                row["sale_date"],
                row["region"],
                row["category"],
                row["product"],
                row["customer_id"],
                row["quantity"],
                row["unit_price"],
                row["revenue"]
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

    print("New dataset loaded into MySQL successfully.")
    print("Rows loaded:", len(df))


if __name__ == "__main__":
    load_csv_to_mysql()