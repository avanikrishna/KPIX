from database import load_sales_data
from kpi import calculate_kpis


df = load_sales_data()

kpis = calculate_kpis(df)

kpi_data = {
    "Metric": [
        "Total Sales",
        "Total Revenue",
        "Average Sale",
        "Total Quantity",
        "Unique Customers"
    ],
    "Value": [
        kpis["total_sales"],
        kpis["total_revenue"],
        kpis["average_sale"],
        kpis["total_quantity"],
        kpis["unique_customers"]
    ]
}

import pandas as pd

kpi_df = pd.DataFrame(kpi_data)

kpi_df.to_csv(
    "output/kpi_summary.csv",
    index=False
)

print("KPI summary exported successfully.")
print(kpi_df)
