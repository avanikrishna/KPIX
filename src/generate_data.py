import pandas as pd
import random
from datetime import datetime, timedelta


def generate_sales_data(filename="data/sales.csv", rows=5000):

    regions = ["North", "South", "East", "West"]
    categories = ["Electronics", "Furniture", "Clothing", "Groceries"]

    products = {
        "Electronics": ["Laptop", "Phone", "Tablet", "Monitor"],
        "Furniture": ["Chair", "Table", "Sofa", "Desk"],
        "Clothing": ["Shirt", "Jeans", "Jacket", "Shoes"],
        "Groceries": ["Rice", "Oil", "Sugar", "Flour"]
    }

    start_date = datetime(2024, 1, 1)

    data = []

    for i in range(rows):

        category = random.choice(categories)
        product = random.choice(products[category])

        quantity = random.randint(1, 10)
        unit_price = random.randint(100, 50000)

        revenue = quantity * unit_price

        sale_date = start_date + timedelta(
            days=random.randint(0, 730)
        )

        data.append({
            "sale_date": sale_date.strftime("%Y-%m-%d"),
            "region": random.choice(regions),
            "category": category,
            "product": product,
            "customer_id": random.randint(1000, 9999),
            "quantity": quantity,
            "unit_price": unit_price,
            "revenue": revenue
        })

    df = pd.DataFrame(data)

    df.to_csv(filename, index=False)

    print(f"Generated {rows} sales records.")
    print(f"Saved to {filename}")


if __name__ == "__main__":
    generate_sales_data()